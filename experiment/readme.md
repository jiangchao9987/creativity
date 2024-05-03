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


[202404301300] change the cmd template( folder to folder , or file to file  , adding abs or relative address mode)


example

'''
!python  /kaggle/working/function/get_answers.py   \
--model_name mistralai/Mistral-7B-Instruct-v0.2     \
--dataset_file /kaggle/working/annotation           \
--task_config short_idea                            \
--file_mode directory         \
--is_abs_mode absolute         \

'''

'''  # be sure in the father dir of annotation   \
!python  /kaggle/working/function/get_answers.py   \
--model_name mistralai/Mistral-7B-Instruct-v0.2     \
--dataset_file annotation           \  
--task_config short_idea                            \
--file_mode directory         \
--is_abs_mode relative         \

'''


'''
!python  /kaggle/working/function/get_answers.py   \
--model_name mistralai/Mistral-7B-Instruct-v0.2     \
--dataset_file /kaggle/working/annotation/WritingPrompts_annotated.json          \
--task_config short_idea                            \
--file_mode file         \
--is_abs_mode absolute         \

'''

'''# be sure in the father dir of annotation           \
!python  /kaggle/working/function/get_answers.py         \
--model_name mistralai/Mistral-7B-Instruct-v0.2          \
--dataset_file annotation/WritingPrompts_annotated.json               \ 
--task_config short_idea                                \
--file_mode file           \
--is_abs_mode relative          \

'''