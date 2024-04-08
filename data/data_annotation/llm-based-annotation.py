# Description: Annotate data with a LLM
# We use LLMs to annotate our plain data crawled from reddit.
# For each post, we use LLMs to judge whether it is a question requries creative answers. (A/B binary classification).
# For each comment, we use LLMs to judge whether it is a creative answer to the question. (A/B binary classification too).

from transformers import AutoTokenizer, AutoModelForCausalLM
import argparse
import json
from tqdm import tqdm
import torch

def arg_parser():
    parser = argparse.ArgumentParser(description='Annotate data with a LLM')
    parser.add_argument('--model_name', type=str, required=True, help='Model name on HF Hub')
    parser.add_argument('--dataset_file', type=str, required=True, help='The crawled data file')
    parser.add_argument('--output_file', type=str, required=True, help='The output file')
    parser.add_argument('--task_name', choices=['question_annotation', 'answer_annotation'], required=True, help='Task name')
    return parser

def load_model(model_name):
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        device_map='auto',
        torch_dtype='auto',
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

def load_data(dataset_file):
    # load a jsonl file
    with open(dataset_file, 'r') as f:
        data = [json.loads(line) for line in f]
    return data

def save_data(data, output_file):
    # save a jsonl file
    with open(output_file, 'w') as f:
        for example in data:
            f.write(json.dumps(example) + '\n')

def build_prompt(
    task_name,
    data_examples,
):
    if task_name == 'question_annotation':
        # prompt need to be tuned according LLMs
        prompt = "Is the following a question that requires creative answers?\n\nTitle: {post_title}\n{post_main_text}\n\nChoose A or B as your answer. A: Yes, it requires creative answers. B: No, it does not require creative answers. Your answer: "
        options = ['A', 'B']
    else:
        raise ValueError(f"Unknown task name: {task_name}")
    
    prompts = [
        prompt.format(
            post_title=example['post_title'],
            post_main_text=example['post_main_text'],
        )
        for example in data_examples
    ]

    return prompts, options

if __name__ == '__main__':

    args = arg_parser().parse_args()

    model, tokenizer = load_model(args.model_name)

    dataset = load_data(args.dataset_file)
    prompts, options = build_prompt(args.task_name, dataset)

    option_ids = [tokenizer.convert_tokens_to_ids(option) for option in options]
    new_dataset = []
    for prompt, example in tqdm(zip(prompts, dataset)):
        with torch.no_grad():
            inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
            outputs = model(**inputs)

            logits = outputs.logits
            option_logits = logits[:, -1, option_ids]
            option_probs = torch.softmax(option_logits, dim=-1)
            most_likely_option = options[option_probs.argmax().item()]
        
        example['llm_annotation'] = most_likely_option
        new_dataset.append(example)
    
    save_data(new_dataset, args.output_file)
    print(f"Annotated data saved to {args.output_file}")