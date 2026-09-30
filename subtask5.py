import os
import urllib.request

# Download the fallback builds (no-avx and standard avx)
FALLBACK_URLS = {
    # Basic AVX (for 2011-2013 Xeon E5 v1/v2)
    "llama_win_avx.zip": "https://github.com/ggml-org/llama.cpp/releases/download/b4372/llama-b4372-bin-win-avx-x64.zip",
    # Universal fallback (Runs on ANY 64-bit CPU, even without AVX)
    "llama_win_noavx.zip": "https://github.com/ggml-org/llama.cpp/releases/download/b4372/llama-b4372-bin-win-noavx-x64.zip",
}

for name, url in FALLBACK_URLS.items():
    dest = os.path.join("./staging_base", name)
    if not os.path.exists(dest):
        print(f"Fetching fallback binary: {name}...")
        urllib.request.urlretrieve(url, dest)