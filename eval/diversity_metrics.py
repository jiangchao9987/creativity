from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import evaluate

def distinct_1(sentence_list):
    char_set = set()
    all_unigram_count = 0
    for line in sentence_list:
        line = line.strip().split(" ")
        sent = ""
        for word in line:
            sent += word
        for char in sent:
            char_set.add(char)
        all_unigram_count += len(sent)
    distinct_unigram_count = len(char_set)

    distinct_1_score=distinct_unigram_count / all_unigram_count
    return distinct_1_score


sp="#####"
def distinct_2(sentence_list):
    bichar_set = set()
    all_bigram_count = 0
    for line in sentence_list:
        line = line.strip().split(" ")
        sent = ""
        for word in line:
            sent += word
        char_len = len(sent)
        for idx in range(char_len - 1):
            bichar_set.add(sent[idx] + sp + sent[idx + 1])
        bichar_set.add("<BOS>" + sp + sent[0])
        bichar_set.add(sent[char_len - 1] + sp + "<EOS>")
        all_bigram_count += (char_len + 1)

    distinct_bigram_count = len(bichar_set)

    distinct_2=distinct_bigram_count / all_bigram_count
    return distinct_2