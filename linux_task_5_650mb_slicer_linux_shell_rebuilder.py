#!/usr/bin/env python3
"""
linux_task5_chunker.py
Packages all Linux staged directories into multi-volume 650 MB tar chunks
for burning onto 700 MB CD-RWs. Generates MD5 checksums and native Linux bash
reassembly scripts (cat *.part_* | tar -xzvf -).
"""

import hashlib
import os
import tarfile

CHUNK_SIZE = 650 * 1024 * 1024  # 650 MB slice threshold
OUTPUT_DIR = os.path.abspath("./linux_cd_ready_chunks")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGETS = [
    ("./linux_staging_base", "bundle_linux_base"),
    ("./linux_staging_wheels", "bundle_linux_wheels"),
    ("./linux_staging_models", "bundle_linux_models"),
    ("./linux_staging_docs", "bundle_linux_docs"),
]


def calculate_md5(filepath):
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def bundle_and_split(source_dir, bundle_name):
    if not os.path.exists(source_dir):
        print("[!] Target directory {} not found. Skipping.".format(source_dir))
        return

    temp_tar = os.path.join(OUTPUT_DIR, "{}.tar.gz".format(bundle_name))
    print("[+] Compressing '{}' into {}...".format(source_dir, temp_tar))

    with tarfile.open(temp_tar, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

    part_num = 1
    checksums = []
    print("[+] Slicing {} into 650 MB parts...".format(os.path.basename(temp_tar)))

    with open(temp_tar, "rb") as src:
        while True:
            chunk = src.read(CHUNK_SIZE)
            if not chunk:
                break
            part_name = "{}.part_{:03d}".format(bundle_name, part_num)
            part_path = os.path.join(OUTPUT_DIR, part_name)
            with open(part_path, "wb") as dst:
                dst.write(chunk)

            md5 = calculate_md5(part_path)
            checksums.append("{}  {}".format(md5, part_name))
            print("    -> Created {} ({:.2f} MB)".format(part_name, len(chunk) / (1024 * 1024)))
            part_num += 1

    os.remove(temp_tar)

    # Write MD5 checksum verification file
    checksum_file = os.path.join(OUTPUT_DIR, "{}_MD5.txt".format(bundle_name))
    with open(checksum_file, "w") as f:
        f.write("\n".join(checksums) + "\n")

    # Generate native Linux bash extraction script
    sh_script = os.path.join(OUTPUT_DIR, "rebuild_{}.sh".format(bundle_name))
    with open(sh_script, "w") as s:
        s.write("#!/bin/bash\nset -e\n")
        s.write("echo 'Validating MD5 checksums...'\n")
        s.write("md5sum -c {}_MD5.txt\n".format(bundle_name))
        s.write("echo 'Combining and extracting {}...'\n".format(bundle_name))
        s.write("cat {}.part_* | tar -xzvf -\n".format(bundle_name))
        s.write("echo '[✓] Extracted {} successfully.'\n".format(bundle_name))

    os.chmod(sh_script, 0o755)
    print("[✓] Finished {}. Outputs in: {}\n".format(bundle_name, OUTPUT_DIR))


if __name__ == "__main__":
    for folder, name in TARGETS:
        bundle_and_split(folder, name)
    print("\n[✓] All Linux bundles sliced and ready for CD-RW burning / Google Drive upload.")