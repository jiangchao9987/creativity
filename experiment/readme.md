# Baselines

You need get the dataset annotated before running the following commands.
see `data/data_annotation/readme.md` for more details.

```
cd creativity
python experiment/get_answer.py \
    --model_name mistralai/Mistral-7B-Instruct-v0.2 \
    --dataset_file data/example-annotated.jsonl \
    --output_path data/answers \
    --task_config short_idea
```

generation configs in `experiment/decoding_configs.py`