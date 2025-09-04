# katana2.py
import subprocess
import json
from collections import Counter, defaultdict
from pathlib import Path
import config

def load_cookie(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

COOKIE = load_cookie(config.COOKIE_FILE)

def run_ffuf_wordlist():
    cmd = [
        "ffuf",
        "-w", config.WORDLIST + ":PATH",
        "-u", f"{config.URL}PATH",
        "-H", f"Cookie: {COOKIE}",
        "-mc", "200-499",
        "-o", config.OUTPUT_FILE_WORDLIST,
        "-of", "json"
    ]
    subprocess.run(cmd, check=True)
    print(f"\n[+] Đã fuzz xong wordlist, lưu output vào {config.OUTPUT_FILE_WORDLIST}")

def normalize_paths(input_json, output_txt):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = data.get("results", [])
    endpoints = defaultdict(list)

    # Gom theo PATH
    for r in results:
        path = r["input"]["PATH"]
        length = r["length"]
        endpoints[path].append(length)

    cleaned = []
    for path, lengths in endpoints.items():
        # Tìm length phổ biến nhất
        default_len = Counter(lengths).most_common(1)[0][0]
        # Nếu có length khác với default_len thì coi là endpoint hợp lệ
        if any(l != default_len for l in lengths):
            if not path.startswith("/"):
                path = "/" + path
            cleaned.append(path)

    cleaned = sorted(set(cleaned))

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned))

    print(f"\n[+] Đã chuẩn hóa: {len(cleaned)} endpoint → {output_txt}")
    return Path(output_txt)

def main():
    run_ffuf_wordlist()
    normalize_paths(config.OUTPUT_FILE_WORDLIST, config.PATH_FILE_WORDLIST)

if __name__ == "__main__":
    main()
