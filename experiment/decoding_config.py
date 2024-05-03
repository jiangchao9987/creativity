from transformers import GenerationConfig
from dataclasses import dataclass

@dataclass
class ShortIdeaGenerationConfig:
    # simple tasks such as commercial slogans, article titles, etc.
    # less than 64 tokens
    max_new_tokens: int = 64
    num_return_sequences: int = 10
    eos_token: str = '\n'
    #pad_token_id: str = ' '

@dataclass
class ShortWritingGenerationConfig:
    # short writing tasks such as jokes, metaphors, etc.
    # less than 512 tokens
    max_new_tokens: int = 512
    num_return_sequences: int = 3
    eos_token: str = '\n'
    #pad_token_id: str = ' '

@dataclass
class LongWritingGenerationConfig:
    # long writing tasks such as stories, essays, etc.
    # less than 2048 tokens
    max_new_tokens: int = 2048

    # set to 1 to avoid memory issues
    # need to run multiple times to get multiple outputs
    num_return_sequences: int = 1
    eos_token: str = '\n'
    #pad_token_id: str = ' '

@dataclass
class DefaultDecodingConfig1:
    do_sample: bool = True
    temperature: float = 1.0

@dataclass
class DefaultSamplingConfig2:
    do_sample: bool = True
    temperature: float = 1.0
    top_k: int = 50

@dataclass
class LexiconDiversityConfig1:
    do_sample: bool = True
    temperature: float = 1.5

@dataclass
class LexiconDiversityConfig2:
    # might lead to memory issues, adjust accordingly
    num_beams: int = 15
    num_beam_groups: int = 5
    diversity_penalty: float = 0.5

