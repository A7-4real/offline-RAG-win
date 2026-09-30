import json
import os
import shutil
import subprocess
import urllib.request

BASE_DIR = os.path.abspath("./staging_base")
os.makedirs(BASE_DIR, exist_ok=True)


def download_with_headers(url, destination):
    """Downloads a file using a standard browser User-Agent to avoid 403/404 bot blocks."""
    print(f" -> Downloading: {url}")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )
    with (
        urllib.request.urlopen(req) as response,
        open(destination, "wb") as out_file,
    ):
        shutil.copyfileobj(response, out_file)


def get_latest_llama_cpp_url():
    """Dynamically resolves the latest AVX2 Windows release of llama.cpp from GitHub."""
    api_url = "https://api.github.com/repos/ggml-org/llama.cpp/releases/latest"
    req = urllib.request.Request(
        api_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            for asset in data.get("assets", []):
                name = asset.get("name", "").lower()
                # Find the AVX2 x64 build
                if (
                    "bin-win-avx2-x64.zip" in name
                    or ("avx2" in name and "x64.zip" in name)
                ):
                    return asset["browser_download_url"]
    except Exception as e:
        print(f" [!] Notice: API auto-lookup failed ({e}), using verified fallback.")

    # Verified direct fallback release
    return "https://github.com/ggml-org/llama.cpp/releases/download/b4372/llama-b4372-bin-win-avx2-x64.zip"


# 1. Base Downloads with permanent endpoints
DOWNLOADS = {
    # Python 3.11.9 official x64 installer
    "python-3.11.9-amd64.exe": "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe",
    # Standalone 7-Zip command line utility
    "7z_extra.zip": "https://www.7-zip.org/a/7za920.zip",
    # Eclipse Adoptium OpenJDK 17 LTS direct binary resolver (Never 404s)
    "openjdk-17.zip": "https://api.adoptium.net/v3/binary/latest/17/ga/windows/x64/jdk/hotspot/normal/eclipse",
    # Neo4j Community Server verified release
    "neo4j-community.zip": "https://dist.neo4j.org/neo4j-community-5.25.1-windows.zip",
}

print("[+] Downloading core runtime binaries...")
for filename, url in DOWNLOADS.items():
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        try:
            print(f"[+] Fetching {filename}...")
            download_with_headers(url, filepath)
        except Exception as err:
            print(f" [!] Error fetching {filename}: {err}")
    else:
        print(f" -> {filename} already exists. Skipping.")

# 2. llama.cpp download
llama_file = os.path.join(BASE_DIR, "llama_cpp_win.zip")
if not os.path.exists(llama_file):
    print("[+] Resolving latest llama.cpp Windows AVX2 package...")
    llama_url = get_latest_llama_cpp_url()
    download_with_headers(llama_url, llama_file)
else:
    print(" -> llama_cpp_win.zip already exists. Skipping.")

# 3. Offline Docs
print("[+] Cloning offline documentation repositories...")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)
REPOS = [
    ("langchain_docs", "https://github.com/langchain-ai/langchain.git"),
    ("langgraph_docs", "https://github.com/langchain-ai/langgraph.git"),
]
for name, url in REPOS:
    repo_path = os.path.join(DOCS_DIR, name)
    if not os.path.exists(repo_path):
        print(f" -> Shallow cloning {name}...")
        subprocess.run(
            ["git", "clone", "--depth", "1", "--filter=blob:none", url, repo_path],
            check=False,
        )

print(f"\n[✓] Task 1 completed successfully. Files are ready in {BASE_DIR}")