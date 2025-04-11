import shutil
from transformers import AutoTokenizer, AutoModelForCausalLM

# Custom cache directory
cache_dir = "C:/Users/yashs/.cache/huggingface"
shutil.rmtree(cache_dir)  # This deletes the cache

print(f"Cache cleared at: {cache_dir}")
