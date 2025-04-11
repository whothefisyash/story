import argparse
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from optimum.exporters.onnx import main_export

def convert_to_gguf(model_path, outtype):
    # Create a temporary ONNX directory
    onnx_dir = os.path.join(model_path, "onnx")
    os.makedirs(onnx_dir, exist_ok=True)

    # Export to ONNX using optimum
    print("📦 Exporting model to ONNX...")
    main_export(
        model_path=model_path,
        output=onnx_dir,
        task="text-generation",
        no_post_process=True
    )

    # Use llama.cpp or another GGUF tool to convert ONNX to GGUF
    print(f"ONNX export complete: {onnx_dir}")
    print("Now use llama.cpp's conversion script to convert ONNX to GGUF.")
    print("Example: ./convert.py --onnx-path <onnx_dir> --outfile model.gguf --outtype", outtype)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Path to HuggingFace model")
    parser.add_argument("--outtype", type=str, default="q4_0", help="Quantization type (e.g., q4_0, q8_0)")
    args = parser.parse_args()

    convert_to_gguf(args.model, args.outtype)
