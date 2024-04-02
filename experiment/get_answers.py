from transformers import AutoTokenizer, AutoModelForCausalLM

def arg_parser():
    import argparse
    parser = argparse.ArgumentParser(description='Get answers from a model')
    parser.add_argument('--model_name', type=str, required=True, help='Model name')
    parser.add_argument('--input_text', type=str, required=True, help='Input text')
    parser.add_argument('--max_length', type=int, default=100, help='Max length of output text')
    parser.add_argument('--num_return_sequences', type=int, default=1, help='Number of return sequences')
    parser.add_argument('--temperature', type=float, default=1.0, help='Temperature')
    parser.add_argument('--top_k', type=int, default=50, help='Top k')
    parser.add_argument('--top_p', type=float, default=1.0, help='Top p')
    parser.add_argument('--repetition_penalty', type=float, default=1.0, help='Repetition penalty')
    parser.add_argument('--num_beams', type=int, default=1, help='Number of beams')
    parser.add_argument('--length_penalty', type=float, default=1.0, help='Length penalty')
    parser.add_argument('--no_repeat_ngram_size', type=int, default=0, help='No repeat ngram size')
    parser.add_argument('--device', type=str, default='cuda', help='Device')
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
            dtype='auto',
        )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

if __name__ == '__main__':
