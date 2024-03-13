# TO-DO List

## Data

- [x] Reddit crawler
- [ ] subreddits
  - [ ] BrainStorming
    - [ ] r/AskEngineers
    - [ ] r/financialindependence
    - [ ] r/Entrepreneur
    - [ ] r/smallbusiness
    - [ ] r/lifehacks
    - [ ] r/productivity
    - [ ] r/GetMotivated
    - [ ] r/GetStudying
    - [ ] r/Cooking
  - [ ] Creative Writing
    - [ ] r/fantasywriters
    - [ ] r/WritingPrompts
    - [ ] r/ShortStories
    - [ ] r/Jokes


## Models

- [x] Base LLM
- [x] LLMs with SFT and RLHF 
- [ ] Fine-tuned with creative dataset

## Decoding methods

### Exsisting/Baselines

- [x] repetition penalty
- [ ] [https://aclanthology.org/2023.acl-long.34.pdf](https://aclanthology.org/2023.acl-long.34.pdf)
- [ ] NS-FH [https://aclanthology.org/2023.acl-demo.6.pdf](https://aclanthology.org/2023.acl-demo.6.pdf)
- [ ] Contrastive decoding ? [https://openreview.net/pdf?id=V88BafmH9Pj](https://openreview.net/pdf?id=V88BafmH9Pj)
- [x] Samplaing temperature

### Ours

- [ ] semantic diverse beam search
- [ ] AI Feedbacks
- [ ] Random words in prompts
- [ ] Model ensembling
  - [ ] ranking
  - [ ] voting
- [ ] NLTK topic normalisation

## Metrics

- [ ] lexcial diversity
  - [ ] Diverse-N Grams
  - [ ] output distribution (entropy?) or Kurtosis/Skewness?
- [ ] semantic diversity
  - [ ] embedding model for semantic similarity comparison (SimCSE/SensentenceBERT?)


# Related Works

- [ ] [https://aclanthology.org/W19-2311.pdf](https://aclanthology.org/W19-2311.pdf)
- [ ] [https://aclanthology.org/2023.emnlp-main.31.pdf](https://aclanthology.org/2023.emnlp-main.31.pdf)
- [ ] [https://openreview.net/pdf?id=SJeYe0NtvH](https://openreview.net/pdf?id=SJeYe0NtvH)