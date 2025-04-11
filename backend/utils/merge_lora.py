from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

#  Paths
base_model_path = "D:/Ahh/Projects/story/models/phi-2"
lora_model_path = "D:/Ahh/Projects/story/models/phi2-lora-checkpoint/phi2-lora-output/checkpoint-100"
merged_model_path = "D:/Ahh/Projects/story/models/phi2-lora-merged"

# Load base model in fp16 or bf16 if you use GPU
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    torch_dtype=torch.float32,  # Use float16 if you have GPU
    device_map="cpu"            # Change to "auto" if GPU is available
)

#  Load LoRA adapter on top of base model
model = PeftModel.from_pretrained(base_model, lora_model_path)

#  Merge LoRA weights into base model
model = model.merge_and_unload()

#  Save the merged model
model.save_pretrained(merged_model_path)

#  Save tokenizer (needed for inference)
tokenizer = AutoTokenizer.from_pretrained(base_model_path)
tokenizer.save_pretrained(merged_model_path)

print(f" Merged model saved to: {merged_model_path}")
