import os
import json
from tqdm import tqdm
import re
from nltk.tokenize import word_tokenize
from nltk.translate import meteor_score
import requests
import numpy as np

Bing_API_Key = os.environ.get('Bing_Key')

def bing_search_query(query, id_ = None, cache = True):
    search_url = "https://api.bing.microsoft.com/v7.0/search"

    headers = {"Ocp-Apim-Subscription-Key": Bing_API_Key}
    params = {"q": query, "textDecorations": True, "textFormat": "HTML", 'responseFilter': 'Webpages'}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    if cache:
        with open(f'bing_search/{id_}.json', 'w') as f:
            json.dump(search_results, f)
    
    return search_results

def process_search_results(search_results):
    # search_results is a dict

    def process_snippet(snippet, query):
        # consider only snippets

        fragments = snippet.split('...')
        fragments = [fragment.strip() for fragment in fragments]

        match_string = []
        tokenized_query = word_tokenize(query)
        meteors = []
        for fragment in fragments:
            matchs = list(re.finditer(r'<b>(.*?)</b>', fragment))
            match_s = ' '.join([match.group(1) for match in matchs])
            match_string.append(match_s)

            meteor = meteor_score.single_meteor_score(tokenized_query, word_tokenize(match_s), alpha=0)
            meteors.append(meteor)
        
        return max(meteors), match_string[np.argmax(meteors)]

            
    query = search_results['queryContext']['originalQuery']
    for page in search_results['webPages']['value']:
        name = page['name']
        url = page['url']
        snippet = page['snippet']
        score, match_string = process_snippet(snippet, query)
        print(f'{query} || {match_string} || {score}\n')
    
    return


if __name__ == "__main__":
    
    prompts = [
        # some metaphors
        "the sun is a dumpling hanging in the sky.",
        "the sun is a fireball in the sky.",
    ]

    for index, line in enumerate(tqdm(prompts)):
        results = bing_search_query(line, id_ = index, cache = True)
        process_search_results(results)
