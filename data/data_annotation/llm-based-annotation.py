# Description: Annotate data with a LLM
# We use LLMs to annotate our plain data crawled from reddit.
# For each post, we use LLMs to judge whether it is a question requries creative answers. (A/B binary classification).
# For each comment, we use LLMs to judge whether it is a creative answer to the question. (A/B binary classification too).

from transformers import AutoTokenizer, AutoModelForCausalLM
#from huggingface_hub import notebook_login
import argparse
import json
from tqdm import tqdm
import torch
import os

def arg_parser():

    parser = argparse.ArgumentParser(description='Annotate data with a LLM')
    parser.add_argument('--model_name', type=str, required=True, help='Model name on HF Hub')
    parser.add_argument('--dataset_file', type=str, required=True, help='The crawled data file')   # abs  , relative dir = os.getcwd() + input dir
    #parser.add_argument('--output_file', type=str, required=True, help='The output file')          # automatically output file name
    parser.add_argument('--task_name',  choices=['question_annotation', 'answer_annotation'], required=True, help='Task name')
    parser.add_argument('--file_mode',  choices=['file', 'directory'], required=True, help='Is a file or a directory')  #
    parser.add_argument('--is_abs_mode',choices=['absolute', 'relative'], required=True, help='Is a file or a directory in a absolute address name')  #        will be modified soon
    return parser

def load_model(model_name):
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        use_auth_token='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',
        device_map='auto',
        torch_dtype=torch.float16,
        #torch_dtype='auto',#   torch_dtype=torch.float16,  for kaggle

    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

def load_data(dataset_file):
    # load a jsonl file
    with open(dataset_file, 'r') as f:
        data = [json.loads(line) for line in f] #[post, post, ...]
    return data

def save_data(data, output_file):     # data = [post, post, ...]
    # save a jsonl file
    with open(output_file, 'w') as f:
        for example in data: #example is a post(submission)
            f.write(json.dumps(example) + '\n')

def build_prompt(
    task_name,
    data_examples, #[post , post...]
):
    if task_name == 'question_annotation':
        # prompt need to be tuned according LLMs
        prompt = "Is the following a question that requires creative answers?\n\n\
Title: {post_title}\n{post_main_text}\n\nChoose A or B as your answer. \
A: Yes, it requires creative answers. B: No, it does not require creative answers. Your answer: "
        options = ['A', 'B']
    else:
        raise ValueError(f"Unknown task name: {task_name}")
    #print(data_examples[0]["post_comments"])
    prompts = []
    align_dataset=[]
    for example in data_examples:
        prompts.append(
            prompt.format(
                post_title= example['post_title'],
                post_main_text= example["text"],
            )
        )
        align_dataset.append({'post_title': example['post_title'] , "post_main_text":example["text"]})

    return prompts, align_dataset,options

if __name__ == '__main__':

    args = arg_parser().parse_args()
    output_dir="annotation"

    model, tokenizer = load_model(args.model_name)
    file_mode = args.file_mode


    file_list =[]
    output_name_list=[]

    input_name = args.dataset_file
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
                    fullname_one_outfile=os.path.join(new_output_dir, f'{file_name}_annotated{file_ext}')
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
        fullname_one_outfile = os.path.join( new_output_dir,f'{file_name}_annotated{file_ext}')
        output_name_list.append(fullname_one_outfile)
        print('file mode an output file:', fullname_one_outfile)

    # use zip to make two lists aligned
    pair_addr_list = zip(file_list,output_name_list )

    for pair_addr in pair_addr_list:


        dataset = load_data(pair_addr[0]) # directed to new dir where datasets are
                                            # dataset_file is a .json file
                                             # [post, post, ...] from one reddit



        prompts, align_dataset, options = build_prompt(args.task_name, dataset) #dataset=[ post , post ,...]


        option_ids = [tokenizer.convert_tokens_to_ids(option) for option in options]
        new_dataset = []
        for prompt, example in tqdm(zip(prompts, align_dataset)): # prompt= a string, example= {'post_title': , "post_main_text": }
            with torch.no_grad():
                inputs = tokenizer(prompt, return_tensors='pt').to(model.device)  # 1-d string
                outputs = model(**inputs)

                logits = outputs.logits  #torch.Size([1, 133(len of inputs) , 32000(volume of dict)])
                option_logits = logits[0, -1, option_ids] # the last vocab of output
                option_probs = torch.softmax(option_logits, dim=-1) #option_logits 1-d tensor
                most_likely_option = options[option_probs.argmax().item()]# argmax(default='')  default='' means flatten the tensor into 1-d

            example['llm_annotation'] = most_likely_option
            new_dataset.append(example) # one dict


        save_data(new_dataset,pair_addr[1] ) #[ dict,dict,dict]
        print(f"Annotated data saved to {pair_addr[1]}")
