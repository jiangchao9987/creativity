# Use LLMs for data annotation/washing

用LLM来进行数据标注/清洗，从我们reddit收集的数据中找到有用的问题。

具体来说就是需要creativity的一些问题。

需要针对不同模型调整prompt。

```
cd creativity
python data/data_annotation/llm-based-annotation.py \
    --model_name mistralai/Mistral-7B-Instruct-v0.2 \
    --dataset_file data/example.jsonl \
    --output_file data/example-annotated.jsonl
    --task_name question_annotation
```

