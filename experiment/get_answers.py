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
    parser.add_argument('--output_path', type=str, required=True, help='Output path')
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
        dataset = [json.loads(line) for line in f]
    return dataset

def load_model(model_name):
    if flash_attn_available(model_name):
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            device_map='auto',
            dtype='auto',
            attn_implementation="flash_attention_2",
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            device_map='auto',
            torch_dtype='auto',
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
        prompt = default_prompt.format(
            title=example['post_title'],
            main_text=example['post_main_text'],
        )
        inputs = tokenizer(prompt, return_tensors='pt')

        inputs = inputs.to(model.device)
        outputs = model.generate(
            **inputs,
            generation_config=generation_config,
        )
        new_tokens_in_output = outputs[:, inputs['input_ids'].shape[-1]:]
        answers = tokenizer.batch_decode(new_tokens_in_output, skip_special_tokens=True)
        
        new_example = example.copy()
        new_example['answers'] = answers
        all_answers.append(new_example)
    return all_answers

if __name__ == '__main__':
    parser = arg_parser()
    args = parser.parse_args()
    model_name = args.model_name
    dataset_file = args.dataset_file
    output_path = args.output_path

    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    model, tokenizer = load_model(model_name)
    dataset = load_dataset_file(dataset_file)

    task_config = task_configs[args.task_config]
    for decoding_config in decoding_configs:
        config = merge_configs(task_config, decoding_configs[decoding_config])
        print(f"Task: {args.task_config}, Decoding: {decoding_config}")

        generation_config = GenerationConfig(**config)
        answers = get_answers(
            model,
            tokenizer,
            dataset,
            generation_config,
        )

        experiment_name = f'{args.task_config}_{decoding_config}'
        output_file = os.path.join(output_path, f'{experiment_name}.jsonl')
        save_answers(answers, output_file)
        print(f"Answers saved to {output_file}")

    print("All experiments done.")