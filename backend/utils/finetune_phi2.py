import os
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType
import torch

# Load dataset
dataset_path = "D:/Ahh/Projects/story/datasets/cleaned_dataset.json"
dataset = load_dataset("json", data_files=dataset_path, split="train")

# Load tokenizer and model
model_path = "D:/Ahh/Projects/story/models/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# ✅ Fix: Assign pad_token
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="auto")


# Apply LoRA (for faster/efficient finetuning)
peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    task_type=TaskType.CAUSAL_LM,
    lora_dropout=0.05,
    bias="none",
    inference_mode=False
)
model = get_peft_model(model, peft_config)

# Preprocess
def tokenize_function(example):
    result = tokenizer(
        f"{example['prompt']}\n\n{example['text']}",
        padding="max_length",
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )
    return {
        "input_ids_new": result["input_ids"][0],
        "attention_mask_new": result["attention_mask"][0]
    }


dataset.cleanup_cache_files()  # clear any cached tokenized data

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    load_from_cache_file=False,
    remove_columns=dataset.column_names
)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Training setup
training_args = TrainingArguments(
    output_dir="D:/Ahh/Projects/story/models/phi-2-finetuned",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    save_steps=500,
    logging_steps=50,
    learning_rate=5e-5,
    fp16=True,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,
)

# Fine-tune
trainer.train()

# Save model
trainer.save_model("D:/Ahh/Projects/story/models/phi-2-finetuned")
