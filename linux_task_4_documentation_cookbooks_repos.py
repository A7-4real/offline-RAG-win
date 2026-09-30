#!/usr/bin/env python3
"""
linux_task4_docs.py
Clones full repositories, agent cookbooks, tools, LLaMA-Factory,
and downloads the complete offline Python 3.11 HTML docset.
"""

import os
import shutil
import subprocess
import urllib.request

DOCS_DIR = os.path.abspath("./linux_staging_docs")
os.makedirs(DOCS_DIR, exist_ok=True)

REPOS = [
    # Agent Frameworks & Tool Repos
    ("crewAI_core", "https://github.com/crewAIInc/crewAI.git"),
    ("crewAI_tools", "https://github.com/crewAIInc/crewAI-tools.git"),
    ("crewAI_examples", "https://github.com/crewAIInc/crewAI-examples.git"),
    ("langchain_core", "https://github.com/langchain-ai/langchain.git"),
    ("langgraph_engine", "https://github.com/langchain-ai/langgraph.git"),
    ("LLaMA_Factory", "https://github.com/hiyouga/LLaMA-Factory.git"),
    # Practical Cookbooks & Patterns
    ("rag_from_scratch", "https://github.com/langchain-ai/rag-from-scratch.git"),
    ("anthropic_agent_cookbook", "https://github.com/anthropics/anthropic-cookbook.git"),
]

print("[+] Shallow cloning agent frameworks and example repositories...")
for folder_name, git_url in REPOS:
    dest = os.path.join(DOCS_DIR, folder_name)
    if not os.path.exists(dest):
        print(" -> Cloning {}...".format(folder_name))
        subprocess.run(["git", "clone", "--depth", "1", git_url, dest], check=False)
    else:
        print(" -> {} already exists. Skipping.".format(folder_name))

# Resilient Python 3.11 HTML Offline Documentation Downloader
PY_DOCS_TAR = os.path.join(DOCS_DIR, "python-3.11-docs-html.tar.bz2")
PY_DOCS_URLS = [
    "https://www.python.org/ftp/python/doc/3.11.9/python-3.11.9-docs-html.tar.bz2",
    "https://docs.python.org/3/archives/python-3.11-docs-html.tar.bz2",
]

if not os.path.exists(PY_DOCS_TAR):
    print("\n[+] Downloading complete offline Python 3.11 HTML documentation...")
    req_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    for url in PY_DOCS_URLS:
        try:
            print(" -> Trying: {}".format(url))
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req) as resp, open(PY_DOCS_TAR, "wb") as f_out:
                shutil.copyfileobj(resp, f_out)
            print(" -> Python docs successfully downloaded.")
            break
        except Exception as e:
            print("    [!] Mirror failed ({}). Trying next...".format(e))
else:
    print(" -> Python docs tarball already present. Skipping.")

print("\n[✓] Linux Task 4 complete. Docs staged in: {}".format(DOCS_DIR))