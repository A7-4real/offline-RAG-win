import os
import subprocess
import sys

BASE_DIR = r"D:\CS\offl_agentic"
STAGE_DIR = os.path.join(BASE_DIR, "staging_llama_factory")
REPO_DIR = os.path.join(STAGE_DIR, "LLaMA-Factory")
WHEELS_DIR = os.path.join(STAGE_DIR, "wheels")

os.makedirs(STAGE_DIR, exist_ok=True)
os.makedirs(WHEELS_DIR, exist_ok=True)

# 1. Clone LLaMA-Factory repository (source code, WebUI, and docs)
REPO_URL = "https://github.com/hiyouga/LLaMA-Factory.git"

if not os.path.exists(REPO_DIR):
    print(f"[+] Cloning LLaMA-Factory (shallow clone)...")
    res = subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, REPO_DIR],
        capture_output=True,
        text=True,
    )
    if res.returncode == 0:
        print(" -> Successfully cloned LLaMA-Factory repository and docs.")
    else:
        print(f" [!] Git clone failed: {res.stderr}")
else:
    print(" -> LLaMA-Factory repository already present. Skipping clone.")

# 2. Key Python dependencies for LLaMA-Factory on Windows 10
# Covers training orchestration, LoRA/PEFT, dataset formatting, and WebUI
LLAMA_FACTORY_PACKAGES = [
    "transformers>=4.41.2",
    "peft>=0.11.1",
    "trl>=0.8.6",
    "accelerate>=0.30.1",
    "datasets>=2.19.1",
    "gradio>=4.31.0",
    "scipy",
    "sentencepiece",
    "protobuf",
    "einops",
    "pyyaml",
    "fire",
    "tensorboard",
]

req_path = os.path.join(STAGE_DIR, "llama_factory_requirements.txt")
with open(req_path, "w") as f:
    f.write("\n".join(LLAMA_FACTORY_PACKAGES) + "\n")

print(f"\n[+] Downloading Windows x64 binary wheels for LLaMA-Factory...")
download_cmd = [
    sys.executable,
    "-m",
    "pip",
    "download",
    "--only-binary=:all:",
    "--platform",
    "win_amd64",
    "--python-version",
    "311",
    "--implementation",
    "cp",
    "--abi",
    "cp311",
    "-r",
    req_path,
    "-d",
    WHEELS_DIR,
]

subprocess.run(download_cmd, check=True)
print(f"\n[✓] LLaMA-Factory staging complete in: {STAGE_DIR}")