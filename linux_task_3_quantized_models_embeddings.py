#!/usr/bin/env python3
"""
linux_task3_models.py
Downloads quantized GGUF models (3B coder, 1B instruction) and BGE-small embedding models.
Requires: pip install huggingface_hub
"""

import os
import sys

try:
    from huggingface_hub import hf_hub_download, snapshot_download
except ImportError:
    print("[!] Error: huggingface_hub is required. Install via: pip install huggingface_hub")
    sys.exit(1)

MODELS_DIR = os.path.abspath("./linux_staging_models")
os.makedirs(MODELS_DIR, exist_ok=True)

TARGET_LLMS = [
    # 3B Code 4-bit model
    {
        "repo_id": "Qwen/Qwen2.5-Coder-3B-Instruct-GGUF",
        "filename": "qwen2.5-coder-3b-instruct-q4_k_m.gguf",
    },
    # Secondary 3B 4-bit model
    {
        "repo_id": "bartowski/Llama-3.2-3B-Instruct-GGUF",
        "filename": "Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    },
    # 1B MiniCPM 8-bit model (Fits comfortably in 4GB RAM)
    {
        "repo_id": "openbmb/MiniCPM-1B-sft-gguf",
        "filename": "minicpm-1b-sft-q8_0.gguf",
    },
    # BGE-small GGUF embedding model (Zero-Python embedding via llama.cpp)
    {
        "repo_id": "compilaction/bge-small-en-v1.5-gguf",
        "filename": "bge-small-en-v1.5-q8_0.gguf",
    },
]

print("[+] Downloading GGUF models for offline CPU inference...")
for model in TARGET_LLMS:
    print(" -> Downloading {}...".format(model["filename"]))
    hf_hub_download(
        repo_id=model["repo_id"],
        filename=model["filename"],
        local_dir=MODELS_DIR,
        local_dir_use_symlinks=False,
    )

# Download standard PyTorch/SafeTensors embedding folder for sentence-transformers / FAISS
EMBED_DIR = os.path.join(MODELS_DIR, "bge-small-en-v1.5")
print("\n[+] Downloading raw sentence-transformers folder: BAAI/bge-small-en-v1.5 (~130 MB)...")
snapshot_download(
    repo_id="BAAI/bge-small-en-v1.5",
    local_dir=EMBED_DIR,
    ignore_patterns=["*.msgpack", "*.h5", "*.ot", "*.onnx*"],
    local_dir_use_symlinks=False,
)

print("\n[✓] Linux Task 3 complete. Models saved in: {}".format(MODELS_DIR))