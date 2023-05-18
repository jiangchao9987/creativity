from lyc.utils import self_info
from lyc.visualize import visualise_self_info
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

if __name__ == '__main__':

    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')

    prompts = [
        # some metaphors
        "A metaphor of sun is that: the sun is a dumpling hanging in the sky.",
        "A metaphor of sun is that: the sun is a fireball in the sky.",
        "A metaphor of sun is that: the sun is a golden coin in the sky.",
        "A metaphor of sun is that: the sun smiled upon me.",
        "A metaphor of moon is that: the moon is a silver coin in the sky.",
        "A metaphor of moon is that: the moon is a cake.",
        "A metaphor of stars is that: the stars are diamonds in the sky.",
        "A metaphor of stars is that: the stars are coffee beans.",
        "A metaphor of clouds is that: the clouds are cotton balls in the sky.",
        "A metaphor of clouds is that: the clouds move like a river.",
        "A metaphor of rain is that: the rain is a shower from the sky.",
        "A metaphor of rain is that: the rain is a shower from the sky, it's warm yet cold.",
        "A metaphor of rain is that: the rain is a sad concerto.",
        "A metaphor of rain is that: it's raining cats and dogs.",
    ]

    results = []
    for line in prompts:
        print(line)
        token, info = self_info(line, model, tokenizer, merge=True)
        line = visualise_self_info(token, info, method='markdown')
        results.append(line)
    
    with open('surprise.md', 'w') as f:
        for line in results:
            f.write(line + '\n\n')
    
    print('Done!')