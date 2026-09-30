#!/usr/bin/env python3
"""
linux_task1_runtimes.py
Downloads native Linux x86_64 runtimes, standalone OpenJDK 17, Neo4j Community tarball,
and pre-built Linux AVX2/AVX/no-AVX llama.cpp binaries.
Compatible with Python 3.7+.
"""

import json
import os
import shutil
import urllib.request

BASE_DIR = os.path.abspath("./linux_staging_base")
os.makedirs(BASE_DIR, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def download_file(url, destination):
    print(" -> Downloading: {}".format(url))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        with open(destination, "wb") as f_out:
            shutil.copyfileobj(resp, f_out)


# 1. Core Linux Runtimes & Standalone Services
DOWNLOADS = {
    # Eclipse Adoptium OpenJDK 17 LTS for Linux x64 (Native Neo4j dependency)
    "openjdk-17-linux-x64.tar.gz": "https://api.adoptium.net/v3/binary/latest/17/ga/linux/x64/jdk/hotspot/normal/eclipse",
    # Neo4j Community Server standalone tarball (Runs bare-metal via ./bin/neo4j console)
    "neo4j-community-5.25.1-unix.tar.gz": "https://dist.neo4j.org/neo4j-community-5.25.1-unix.tar.gz",
    # llama.cpp Linux pre-built AVX2 (Primary)
    "llama-bin-linux-avx2.zip": "https://github.com/ggml-org/llama.cpp/releases/download/b4372/llama-b4372-bin-ubuntu-x64.zip",
    # llama.cpp Linux pre-built no-AVX (Universal fallback for legacy Xeon/CPUs)
    "llama-bin-linux-noavx.zip": "https://github.com/ggml-org/llama.cpp/releases/download/b4372/llama-b4372-bin-ubuntu-noavx-x64.zip",
}

print("[+] Downloading Linux x86_64 core runtime binaries and services...")
for filename, url in DOWNLOADS.items():
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        try:
            print("[+] Fetching {}...".format(filename))
            download_file(url, filepath)
        except Exception as err:
            print(" [!] Failed to download {}: {}".format(filename, err))
    else:
        print(" -> {} already exists. Skipping.".format(filename))

print("\n[✓] Linux Task 1 complete. Files stored in: {}".format(BASE_DIR))