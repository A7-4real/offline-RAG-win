import hashlib
import os
import tarfile

CHUNK_SIZE = 650 * 1024 * 1024  # 650 MB
OUTPUT_DIR = os.path.abspath("./cd_chunks")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def calculate_md5(filepath):
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def bundle_and_split(source_dir, bundle_name):
    temp_tar = os.path.join(OUTPUT_DIR, f"{bundle_name}.tar")
    print(f"[+] Archiving '{source_dir}' into {temp_tar}...")
    with tarfile.open(temp_tar, "w") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

    part_num = 1
    checksums = []
    print(f"[+] Splitting {temp_tar} into 650MB slices...")
    with open(temp_tar, "rb") as src:
        while True:
            chunk = src.read(CHUNK_SIZE)
            if not chunk:
                break
            part_name = f"{bundle_name}.part_{part_num:03d}"
            part_path = os.path.join(OUTPUT_DIR, part_name)
            with open(part_path, "wb") as dst:
                dst.write(chunk)

            md5 = calculate_md5(part_path)
            checksums.append(f"{md5}  {part_name}")
            print(f" -> Created {part_name} ({len(chunk)/(1024*1024):.2f} MB)")
            part_num += 1

    os.remove(temp_tar)
    checksum_file = os.path.join(OUTPUT_DIR, f"{bundle_name}_MD5.txt")
    with open(checksum_file, "w") as f:
        f.write("\n".join(checksums))

    # Generate quick reassembly batch file for the air-gapped machine
    batch_script = os.path.join(OUTPUT_DIR, f"rebuild_{bundle_name}.bat")
    with open(batch_script, "w") as b:
        b.write(f"@echo off\n")
        b.write(f"echo Combining chunks for {bundle_name}...\n")
        b.write(f"copy /b {bundle_name}.part_* {bundle_name}.tar\n")
        b.write(f"tar -xf {bundle_name}.tar\n")
        b.write(f"echo [Done] Extracted to current directory.\n")

    print(f"[✓] Completed {bundle_name}. Output in {OUTPUT_DIR}\n")


if __name__ == "__main__":
    # Split each staged component into CD-RW ready slices
    for target, name in [
        ("./staging_base", "bundle_base"),
        ("./staging_wheels", "bundle_wheels"),
        ("./staging_models", "bundle_models"),
    ]:
        if os.path.exists(target):
            bundle_and_split(target, name)