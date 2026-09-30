import os
import sys

# Ensure huggingface_hub is installed: pip install huggingface_hub
from huggingface_hub import hf_hub_download, snapshot_download

MODELS_DIR = os.path.abspath("./staging_models")
os.makedirs(MODELS_DIR, exist_ok=True)

# 1. Quantized LLMs
TARGET_LLMS = [
    {
        "repo_id": "Qwen/Qwen2.5-Coder-3B-Instruct-GGUF",
        "filename": "qwen2.5-coder-3b-instruct-q4_k_m.gguf",
    },
    {
        "repo_id": "bartowski/Llama-3.2-3B-Instruct-GGUF",
        "filename": "Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    },
    {
        "repo_id": "openbmb/MiniCPM-1B-sft-gguf",
        "filename": "minicpm-1b-sft-q8_0.gguf",
    },
    # GGUF version of BGE-small for zero-dependency RAG via llama.cpp
    {
        "repo_id": "compilaction/bge-small-en-v1.5-gguf",
        "filename": "bge-small-en-v1.5-q8_0.gguf",
    },
]

print("[+] Downloading LLMs and GGUF embeddings...")
for model in TARGET_LLMS:
    print(f" -> Downloading {model['filename']} from {model['repo_id']}...")
    hf_hub_download(
        repo_id=model["repo_id"],
        filename=model["filename"],
        local_dir=MODELS_DIR,
        local_dir_use_symlinks=False,
    )

# 2. Standard HuggingFace / Sentence-Transformers embedding model
# (Used directly by LangChain Chroma/FAISS with pure Python offline)
EMBED_DIR = os.path.join(MODELS_DIR, "bge-small-en-v1.5")
print(
    f"[+] Downloading raw sentence-transformer folder: BAAI/bge-small-en-v1.5 (~130 MB)..."
)
snapshot_download(
    repo_id="BAAI/bge-small-en-v1.5",
    local_dir=EMBED_DIR,
    ignore_patterns=["*.msgpack", "*.h5", "*.ot", "*.onnx*"],
    local_dir_use_symlinks=False,
)

print("[✓] Task 3 complete. Models and embeddings saved in ./staging_models")