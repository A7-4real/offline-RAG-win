import os
import subprocess
import sys

WHEELS_DIR = os.path.abspath("./staging_wheels")
os.makedirs(WHEELS_DIR, exist_ok=True)

# Comprehensive dependency list for agentic orchestration, tool-calling, and parsing
REQUIREMENTS = [
    # Core orchestration & multi-agent graphs
    "langchain>=0.3.0",
    "langchain-core",
    "langchain-community",
    "langchain-openai",  # To interface with local llama-server via OpenAI API
    "langgraph",
    "pydantic>=2.0",
    # Document loading, OCR, & document parsing
    "markitdown",
    "pypdf",
    "pdfplumber",
    "python-docx",
    "openpyxl",
    "beautifulsoup4",
    "python-pptx",
    # Knowledge Graph & DB engines
    "neo4j",
    "duckdb",
    "sqlalchemy",
    # Local lightweight vector store & embeddings
    "chromadb",
    "faiss-cpu",
    "sentence-transformers",
    # Tool building, API clients, and execution runtimes
    "httpx",
    "requests",
    "fastapi",
    "uvicorn",
    "websockets",
    "jinja2",
    "tiktoken",
    "rich",
]

req_file = os.path.join(WHEELS_DIR, "requirements.txt")
with open(req_file, "w") as f:
    f.write("\n".join(REQUIREMENTS))

print("[+] Downloading Windows x64 binary wheels for Python 3.11...")
cmd = [
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
    req_file,
    "-d",
    WHEELS_DIR,
]

subprocess.run(cmd, check=True)
print("[✓] Task 2 complete. All wheels downloaded into ./staging_wheels")