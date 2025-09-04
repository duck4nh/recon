import requests
import subprocess
import config
from pathlib import Path

from katana2 import load_cookie

def is_method_supported(status):
    if status in (405, 501):
        return False
    return 200 <= status < 500

def check_method(path, cookie):
    url = f"{config.URL.rstrip('/')}/{path.lstrip('/')}"
    results = {"GET": False, "POST": False}

    try:
        # --- GET ---
        r_get = requests.get(url, headers={"Cookie": cookie}, timeout=8, allow_redirects=False)
        if is_method_supported(r_get.status_code):
            results["GET"] = True
        if "GET" in r_get.headers.get("Allow", "").upper():
            results["GET"] = True

        # --- POST ---
        r_post = requests.post(
            url,
            headers={"Cookie": cookie, "Content-Type": "application/json"},
            timeout=8,
            allow_redirects=False
        )
        if is_method_supported(r_post.status_code):
            results["POST"] = True
        if "POST" in r_post.headers.get("Allow", "").upper():
            results["POST"] = True

    except requests.RequestException as e:
        print(f"[!] Lỗi khi test {url}: {e}")

    return results

def fuzz_params(get_file, post_file, cookie):
    def run_ffuf(cmd):
        subprocess.run(cmd, check=True)

    if Path(get_file).exists():
        run_ffuf([
            "ffuf",
            "-w", f"{config.PARAM_FILE}:PARAM",
            "-w", f"{get_file}:PATH",
            "-u", f"{config.URL}PATH?PARAM=1",
            "-mc", "200-400",
            "-v",
            "-t", "50",
            "-rate", "100",
            "-H", f"Cookie: {cookie}",
            "-o", config.FFUF_GET_WORDLIST_JSON,
            "-of", "json"
        ])
        print(f"[+] Fuzz GET param → {config.FFUF_GET_WORDLIST_JSON}")

    if Path(post_file).exists():
        run_ffuf([
            "ffuf",
            "-w", f"{config.PARAM_FILE}:PARAM",
            "-w", f"{post_file}:PATH",
            "-u", f"{config.URL}PATH",
            "-X", "POST",
            "-d", '{\"PARAM\": \"1\"}',
            "-H", "Content-Type: application/json",
            "-mc", "200-500",
            "-v",
            "-t", "50",
            "-rate", "100",
            "-H", f"Cookie: {cookie}",
            "-o", config.FFUF_POST_WORDLIST_JSON,
            "-of", "json"
        ])
        print(f"[+] Fuzz POST param → {config.FFUF_POST_WORDLIST_JSON}")

def main():
    path_file = Path(config.PATH_FILE_WORDLIST)
    if not path_file.exists():
        print(f"[!] Không tìm thấy {config.PATH_FILE_WORDLIST}, dừng fuzz param")
        return

    with open(path_file, "r", encoding="utf-8") as f:
        paths = [line.strip() for line in f if line.strip()]

    if not paths:
        print("[!] Không có endpoint nào trong paths_wordlist.txt để fuzz")
        return
    
    def load_cookie(file_path):
        """Đọc cookie từ file"""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    cookie = load_cookie(config.COOKIE_FILE)

    get_endpoints = []
    post_endpoints = []

    for path in paths:
        print(f"[*] Test endpoint {path}")
        res = check_method(path, cookie)
        if res["GET"]:
            get_endpoints.append(path)
        if res["POST"]:
            post_endpoints.append(path)

    # Ghi endpoint hợp lệ
    with open(config.GET_FILE_WORDLIST, "w") as f:
        f.write("\n".join(get_endpoints))
    with open(config.POST_FILE_WORDLIST, "w") as f:
        f.write("\n".join(post_endpoints))

    print(f"[+] GET endpoints: {len(get_endpoints)} -> {config.GET_FILE_WORDLIST}")
    print(f"[+] POST endpoints: {len(post_endpoints)} -> {config.POST_FILE_WORDLIST}")

    fuzz_params(config.GET_FILE_WORDLIST, config.POST_FILE_WORDLIST, cookie)

if __name__ == "__main__":
    main()

