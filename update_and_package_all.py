import hashlib
import os
import shutil
import zipfile

BASE_DIR = r"D:\CS\offl_agentic"
CD_CHUNKS_DIR = os.path.join(BASE_DIR, "cd_chunks")
FINAL_ZIP_DIR = os.path.join(BASE_DIR, "drive_cd_ready_zips")
os.makedirs(FINAL_ZIP_DIR, exist_ok=True)

CHUNK_SIZE = 650 * 1024 * 1024  # 650 MB per disc slice


def calculate_md5(filepath):
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def split_file(source_file, bundle_name, output_dir):
    part_num = 1
    checksums = []
    print(f"[+] Slicing {os.path.basename(source_file)} into 650 MB parts...")
    with open(source_file, "rb") as src:
        while True:
            chunk = src.read(CHUNK_SIZE)
            if not chunk:
                break
            part_name = f"{bundle_name}.part_{part_num:03d}"
            part_path = os.path.join(output_dir, part_name)
            with open(part_path, "wb") as dst:
                dst.write(chunk)
            md5 = calculate_md5(part_path)
            checksums.append(f"{md5}  {part_name}")
            print(f"    -> Created {part_name} ({len(chunk) / (1024 * 1024):.2f} MB)")
            part_num += 1

    # Checksum file
    with open(os.path.join(output_dir, f"{bundle_name}_MD5.txt"), "w") as f:
        f.write("\n".join(checksums) + "\n")

    # Windows batch rebuilder
    batch_file = os.path.join(output_dir, f"rebuild_{bundle_name}.bat")
    with open(batch_file, "w") as b:
        b.write(f"@echo off\n")
        b.write(f"echo Combining chunks for {bundle_name}...\n")
        b.write(f"copy /b {bundle_name}.part_* {bundle_name}.zip\n")
        b.write(f"echo [Done] Reassembled {bundle_name}.zip\n")


# 1. Package staging_docs_and_examples into a single ZIP, then split if needed
docs_dir = os.path.join(CD_CHUNKS_DIR, "staging_docs_and_examples")
if os.path.exists(docs_dir):
    temp_docs_zip = os.path.join(FINAL_ZIP_DIR, "temp_bundle_docs.zip")
    print(f"\n[+] Compressing staging_docs_and_examples...")
    with zipfile.ZipFile(temp_docs_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(docs_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, CD_CHUNKS_DIR)
                z.write(abs_path, rel_path)

    split_file(temp_docs_zip, "bundle_docs", FINAL_ZIP_DIR)
    os.remove(temp_docs_zip)

# 2. Package loose tools, PDF, fallback binaries into bundle_extras
extras_files = [
    "Constrained Agentic Systems Architecture Guide.pdf",
    "llama_win_avx.zip",
    "llama_win_noavx.zip",
    "strategy.txt",
]
print(f"\n[+] Packaging architecture PDF and fallback CPU binaries...")
extras_zip = os.path.join(FINAL_ZIP_DIR, "bundle_extras.zip")
with zipfile.ZipFile(extras_zip, "w", zipfile.ZIP_DEFLATED) as z:
    for filename in extras_files:
        p = os.path.join(CD_CHUNKS_DIR, filename)
        if os.path.exists(p):
            z.write(p, filename)
            print(f"    -> Added {filename}")

# 3. Copy existing parts and batch scripts into FINAL_ZIP_DIR
print(f"\n[+] Consolidating pre-chunked base, wheels, and models...")
for item in os.listdir(CD_CHUNKS_DIR):
    if item.endswith((".part_001", ".part_002", ".part_003", "_MD5.txt", ".bat")):
        src = os.path.join(CD_CHUNKS_DIR, item)
        dst = os.path.join(FINAL_ZIP_DIR, item)
        shutil.copy2(src, dst)
        print(f"    -> Synced {item}")

# 4. Generate master burn plan for 700 MB CD-RWs
all_files = sorted(os.listdir(FINAL_ZIP_DIR))
manifest_path = os.path.join(FINAL_ZIP_DIR, "CD_RW_BURN_ORDER.txt")
with open(manifest_path, "w") as m:
    m.write("=== CD-RW BURNING ORDER (700 MB / 650 MB payload limit) ===\n\n")
    disc = 1
    for f in all_files:
        fpath = os.path.join(FINAL_ZIP_DIR, f)
        if f.endswith((".bat", ".txt")) and not f.endswith("_MD5.txt"):
            continue
        size_mb = os.path.getsize(fpath) / (1024 * 1024)
        if size_mb > 0.1:  # skip empty or tiny helpers in separate discs
            m.write(f"Disc {disc:02d}: {f} ({size_mb:.2f} MB)\n")
            disc += 1

print(f"\n[✓] All items processed. Files ready in {FINAL_ZIP_DIR}")
print(f"[✓] Open {manifest_path} to see exact CD-RW burn sequence.")