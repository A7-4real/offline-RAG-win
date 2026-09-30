import os
import shutil
import subprocess
import urllib.request

DOCS_DIR = os.path.abspath("./staging_docs_and_examples")
os.makedirs(DOCS_DIR, exist_ok=True)

# 1. Repositories containing source code, agent examples, and cookbooks
AGENT_REPOSITORIES = [
    # CrewAI source and built-in tools
    ("crewAI_core", "https://github.com/crewAIInc/crewAI.git"),
    ("crewAI_tools", "https://github.com/crewAIInc/crewAI-tools.git"),
    ("crewAI_examples", "https://github.com/crewAIInc/crewAI-examples.git"),
    # LangChain & LangGraph source + docs
    ("langchain_core", "https://github.com/langchain-ai/langchain.git"),
    ("langgraph_engine", "https://github.com/langchain-ai/langgraph.git"),
    # Practical Agent & RAG cookbooks (Jupyter notebooks)
    (
        "rag_from_scratch",
        "https://github.com/langchain-ai/rag-from-scratch.git",
    ),
    (
        "anthropic_agent_cookbook",
        "https://github.com/anthropics/anthropic-cookbook.git",
    ),
]

print("[+] Cloning agent frameworks, cookbooks, and example repositories...")
for folder_name, git_url in AGENT_REPOSITORIES:
    dest_path = os.path.join(DOCS_DIR, folder_name)
    if not os.path.exists(dest_path):
        print(" -> Cloning {}...".format(folder_name))
        # --depth 1 discards git history to save disk and CD space
        res = subprocess.run(
            ["git", "clone", "--depth", "1", git_url, dest_path],
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            print(" [!] Failed cloning {}: {}".format(folder_name, res.stderr))
    else:
        print(" -> {} already present. Skipping.".format(folder_name))

# 2. Official Python 3.11 complete offline documentation (HTML zip)
# Updated Python 3.11 docset download logic
PY_DOCS_ZIP = os.path.join(DOCS_DIR, "python-3.11-docs-html.zip")

# Tested mirrors on python.org:
CANDIDATE_URLS = [
    # 1. Official FTP archive (Permanent for specific releases)
    "https://www.python.org/ftp/python/doc/3.11.9/python-3.11.9-docs-html.zip",
    # 2. General minor release archive
    "https://docs.python.org/3/archives/python-3.11-docs-html.zip",
    # 3. Latest 3.11 maintenance branch snapshot
    "https://www.python.org/ftp/python/doc/current/python-3.11-docs-html.zip",
]

if not os.path.exists(PY_DOCS_ZIP):
    print("\n[+] Downloading complete offline Python 3.11 HTML docset...")
    downloaded = False
    for url in CANDIDATE_URLS:
        try:
            print(f" -> Trying: {url}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp, open(PY_DOCS_ZIP, "wb") as f:
                shutil.copyfileobj(resp, f)
            print(" -> Success! Python 3.11 docset downloaded.")
            downloaded = True
            break
        except Exception as e:
            print(f"    [!] Failed from this URL ({e}), trying next mirror...")

    if not downloaded:
        print(" [X] All official doc mirrors failed. You can manually grab the doc ZIP from:")
        print("     https://www.python.org/doc/versions/")
else:
    print(" -> Python 3.11 docset already exists. Skipping.")