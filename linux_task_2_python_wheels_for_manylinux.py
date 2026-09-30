#!/usr/bin/env python3
"""
linux_task2_wheels.py
Downloads Linux-native (manylinux2014_x86_64) Python 3.11 wheels for LangChain,
LangGraph, CrewAI, LLaMA-Factory, document parsers, and vector databases.
Run this script using Python 3.11.
"""

import os
import subprocess
import sys

WHEELS_DIR = os.path.abspath("./linux_staging_wheels")
os.makedirs(WHEELS_DIR, exist_ok=True)

# Comprehensive Linux dependency list
REQUIREMENTS = [
    # Core Agentic & Graph Orchestration
    "langchain>=0.3.0",
    "langchain-core",
    "langchain-community",
    "langchain-openai",
    "langgraph",
    "crewai>=0.150.0",
    "crewai-tools",
    "pydantic>=2.4.2",
    # Document Loading & Unstructured Parsing
    "markitdown",
    "pypdf",
    "pdfplumber",
    "python-docx",
    "openpyxl",
    "beautifulsoup4",
    "python-pptx",
    # Databases & Vector Stores
    "neo4j",
    "duckdb",
    "sqlalchemy",
    "chromadb",
    "faiss-cpu",
    "sentence-transformers",
    # API Tooling & Execution Engine
    "fastapi",
    "uvicorn",
    "httpx",
    "requests",
    "websockets",
    "jinja2",
    "tiktoken",
    "rich",
    # LLaMA-Factory Core Training & WebUI dependencies
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

req_file = os.path.join(WHEELS_DIR, "linux_requirements.txt")
with open(req_file, "w") as f:
    f.write("\n".join(REQUIREMENTS) + "\n")

print("[+] Downloading Linux x86_64 binary wheels for Python 3.11...")
cmd = [
    sys.executable,
    "-m",
    "pip",
    "download",
    "--only-binary=:all:",
    "--platform",
    "manylinux2014_x86_64",
    "--python-version",
    "311",
    "--implementation",
    "cp",
    "--abi",
    "cp311",
    "-r",
    req_file,
    "-d",
    WHEELS_DIR,
]

try:
    subprocess.run(cmd, check=True)
    print("\n[✓] Linux Task 2 complete. All wheels downloaded into: {}".format(WHEELS_DIR))
except subprocess.CalledProcessError as e:
    print("\n[!] Error downloading wheels: {}".format(e))