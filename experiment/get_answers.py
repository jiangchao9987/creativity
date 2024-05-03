from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM, GenerationConfig
import json
from decoding_config import (
    ShortIdeaGenerationConfig,
    ShortWritingGenerationConfig,
    LongWritingGenerationConfig,
    DefaultDecodingConfig1,
    DefaultSamplingConfig2,
    LexiconDiversityConfig1,
    LexiconDiversityConfig2,
)
from dataclasses import dataclass, asdict
import os
from tqdm import tqdm
import argparse
import torch
task_configs = {
    'short_idea': ShortIdeaGenerationConfig,
    'short_writing': ShortWritingGenerationConfig,
    'long_writing': LongWritingGenerationConfig,
}

decoding_configs = {
    'default1': DefaultDecodingConfig1,
    'default2': DefaultSamplingConfig2,
    'lex_div1': LexiconDiversityConfig1,
    'lex_div2': LexiconDiversityConfig2,
}

default_prompt = """[INST] {title}\n\n{main_text}\n\n[/INST]"""
default_prompt1 = """[INST] Could you come up with some interesting ideas for {title}\n\n\
And its content {main_text}\n\n\
Explain the steps we need to come up with solutions for the above question. And analyze whether these steps require creativity[/INST]"""

def merge_configs(
    config1: dataclass,
    config2: dataclass,
) -> dict:
    config1 = config1()
    config2 = config2()
    merged_config = {**asdict(config1), **asdict(config2)}
    return merged_config

def arg_parser():
    parser = argparse.ArgumentParser(description='Get answers from a model')
    parser.add_argument('--model_name', type=str, required=True, help='Model name')
    parser.add_argument('--dataset_file', type=str, required=True, help='Input text')
    parser.add_argument('--task_config', type=str, required=True, help='generation_config for this task', choices=task_configs.keys())
    #parser.add_argument('--output_path', type=str, required=True, help='Output path')
    parser.add_argument('--file_mode',  choices=['file', 'directory'], required=True, help='Is a file or a directory')  #
    parser.add_argument('--is_abs_mode',choices=['absolute', 'relative'], required=True, help='Is a file or a directory in a absolute address name')  #
    return parser

def flash_attn_available(model_name):
    flash_attn_models = [
        'llama',
        'mistral',
    ]
    for flash_attn_model in flash_attn_models:
        if flash_attn_model in model_name.lower():
            return True
    return False

def is_quantized(model_name):
    if 'gptq' in model_name.lower():
        return True
    return False

def load_dataset_file(dataset_file):
    # load dataset file. jsonl
    with open(dataset_file, 'r') as f:
        dataset = [json.loads(line) for line in f] # [dict{'posttitle':xxx, 'text':xxx , 'annotation':xxx},...]
    return dataset

def load_model(model_name):
    if flash_attn_available(model_name) and 0:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            device_map='auto',
            torch_dtype='auto',
            attn_implementation="flash_attention_2",
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            device_map='auto',
            #torch_dtype='auto',
            torch_dtype=torch.float16, #  for kaggle
        )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

def save_answers(answers, output_file):
    # save a jsonl file
    with open(output_file, 'w') as f:
        for example in answers:
            f.write(json.dumps(example) + '\n')

def get_answers(
    model,
    tokenizer,
    dataset,
    generation_config,
):
    all_answers = []
    for example in tqdm(dataset):

        prompt = default_prompt1.format(
            title=example['post_title'],
            main_text=example['post_main_text'],
        )
        inputs = tokenizer(prompt, return_tensors='pt')

        inputs = inputs.to(model.device)
        outputs = model.generate(
            **inputs,
            generation_config=generation_config,
            pad_token_id=tokenizer.eos_token_id, #for error solved
        )
        new_tokens_in_output = outputs[:, inputs['input_ids'].shape[-1]:] # from the end index of sentence
        #print(inputs['input_ids'].shape, outputs.shape)
        answers = tokenizer.batch_decode(new_tokens_in_output, skip_special_tokens=True)

        new_pair = example.copy()
        new_pair['answers'] = answers
        all_answers.append(new_pair)
    return all_answers

if __name__ == '__main__':
    parser = arg_parser()
    args = parser.parse_args()
    model_name = args.model_name
    file_mode = args.file_mode
    input_name = args.dataset_file #--dataset_file data/example-annotated.jsonl
    #output_path = args.output_path  #--output_path data/answers

    model, tokenizer = load_model(model_name)


    output_dir = "answers"
    file_list =[]
    output_name_list=[]

    task_config = task_configs[args.task_config] #short

    print(args.is_abs_mode)
    if args.is_abs_mode == 'relative':
        input_name = os.path.join(os.getcwd(),input_name)

    #now input_name is in abs, whether it is a file or dir
    print(file_mode)
    if file_mode =='directory':
        #dataset_file is a dir
        count =0
        for dirname, _, filenames in os.walk(input_name):
            if count==0:
                for filename in filenames:
                    fullname_one_file =  os.path.join(dirname, filename)
                    file_list.append(fullname_one_file)
                    print('dir mode an input file:',fullname_one_file)
                    # outfiles name
                    dir_name, full_file_name = os.path.split(fullname_one_file)
                    file_name, file_ext = os.path.splitext(full_file_name)
                    name_seq = file_name.split('_')
                    file_name=name_seq[0]
                    dir1, dir2 = os.path.split(dir_name)
                    new_output_dir = os.path.join(dir1, output_dir)
                    if os.path.exists(new_output_dir) == False:
                        os.mkdir(new_output_dir)
                    fullname_one_outfile=os.path.join(new_output_dir, f'{file_name}{file_ext}')
                    output_name_list.append(fullname_one_outfile)
                    print('dir mode an output file:',fullname_one_outfile)
                count+=1

    elif file_mode=='file':
        #dataset_file is a file
        file_list.append(input_name )
        print('file mode an input file:', input_name)
        # outfile name
        dir_name, full_file_name = os.path.split(input_name )
        file_name, file_ext = os.path.splitext(full_file_name)
        name_seq = file_name.split('_')
        file_name = name_seq[0]

        dir1, dir2 = os.path.split(dir_name)
        new_output_dir = os.path.join(dir1, output_dir)
        if os.path.exists(new_output_dir) == False:
            os.mkdir(new_output_dir)
        fullname_one_outfile = os.path.join( new_output_dir,f'{file_name}{file_ext}')
        output_name_list.append(fullname_one_outfile)
        print('file mode an output file:', fullname_one_outfile)

    # use zip to make two lists aligned
    pair_addr_list = zip(file_list,output_name_list )

    for pair_addr in pair_addr_list:
        for decoding_config in decoding_configs:
            config = merge_configs(task_config, decoding_configs[decoding_config]) # {  max_new_tokens: 64 , num_return_sequences:  10 ,eos_token:  '\n' , ....}
            print(f"Task: {args.task_config}, Decoding: {decoding_config}")

            generation_config = GenerationConfig(**config)
            answers = get_answers(
                model,
                tokenizer,
                load_dataset_file(pair_addr[0]),
                generation_config,
            )

            experiment_suffix = f'_{args.task_config}_{decoding_config}'

            dir_name, full_file_name = os.path.split(pair_addr[1])
            file_name, file_ext = os.path.splitext(full_file_name)
            output_file= os.path.join(dir_name, f'{file_name}{experiment_suffix}{file_ext}')
            save_answers(answers, output_file)
            print(f"Answers saved to {output_file}")

        print(f"experiments of {pair_addr[1]} is done.")