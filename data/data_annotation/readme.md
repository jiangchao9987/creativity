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


[202404301300] change the cmd template ( folder to folder , or file to file  ) 

examples



```
!python  /kaggle/working/function/llm-based-annotation.py   \
--model_name mistralai/Mistral-7B-Instruct-v0.2      \
--dataset_file /kaggle/working/data  \
--task_name question_annotation \
--file_mode directory \
--is_abs_mode absolute      \
```


be sure in the father dir of data 
```                  
!python  /kaggle/working/function/llm-based-annotation.py   \
--model_name mistralai/Mistral-7B-Instruct-v0.2      \
--dataset_file data   \
--task_name question_annotation \
--file_mode directory \
--is_abs_mode relative      \
```

```
!python  /kaggle/working/function/llm-based-annotation.py   \
--model_name mistralai/Mistral-7B-Instruct-v0.2      \
--dataset_file /kaggle/working/data/AskEngineers_after_data_check.json   \
--task_name question_annotation \
--file_mode file \
--is_abs_mode absolute      \
```

be sure in the father dir of data                   
```
!python  /kaggle/working/function/llm-based-annotation.py   \
--model_name mistralai/Mistral-7B-Instruct-v0.2      \
--dataset_file data/AskEngineers_after_data_check.json   \
--task_name question_annotation \
--file_mode file \
--is_abs_mode relative      \
```