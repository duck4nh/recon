import subprocess
from pathlib import Path
from collections import Counter
import urllib.parse
import config


def load_cookie(file_path):
    """Đọc cookie từ file"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

COOKIE = load_cookie(config.COOKIE_FILE)

def run_katana(cmd):
    """Chạy Katana với list cmd"""
    subprocess.run(cmd, check=True)

def filter_paths(input_file, output_file="output.txt", blacklist_ext=None):
    if blacklist_ext is None:
        blacklist_ext = {
            ".js", ".css", ".jpg", ".png", ".gif", ".svg",
            ".json", ".xml", ".txt", ".md"
        }

    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    def normalize_path(url):
        parsed = urllib.parse.urlparse(url)
        path = parsed.path

        if not path:
            return None

        # Bỏ dấu / cuối (trừ khi chỉ có "/")
        if path != "/" and path.endswith("/"):
            path = path[:-1]

        return path

    def is_valid_path(path):
        return not any(path.lower().endswith(ext) for ext in blacklist_ext)

    normalized_paths = []
    duplicates = []

    for line in lines:
        path = normalize_path(line)
        if path and is_valid_path(path):
            if path in normalized_paths:
                duplicates.append(path)
            normalized_paths.append(path)

    # Loại bỏ trùng
    unique_paths = sorted(set(normalized_paths))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(unique_paths))

    print(f"\n[+] Đã lưu {len(unique_paths)} path vào {output_file}")
    if duplicates:
        print(f"\n[!] Phát hiện {len(duplicates)} path trùng lặp (đã loại bỏ)")

    return Path(output_file)

# =========================
# Chạy Katana
# =========================
def main():
    katana_cmd = [
        "katana",
        "-u", config.URL,
        "-headless",
        "-depth", "4",
        "-H", f"Cookie: {COOKIE}",
        "-jsl",
        "-jc",
        "-silent",
        "-o", config.INPUT_FILE
    ]
    run_katana(katana_cmd)
    filter_paths(config.INPUT_FILE, config.OUTPUT_FILE)

if __name__ == "__main__":
    main()
