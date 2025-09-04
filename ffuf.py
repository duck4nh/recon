import requests
import subprocess
import config

# -------- CONFIG --------
base_url = config.URL
input_file = config.OUTPUT_FILE
get_file = config.GET_FILE
post_file = config.POST_FILE
timeout = config.TIMEOUT
STRICT_MODE = config.STRICT_MODE
# ------------------------

def load_cookie(file_path):
    """Đọc cookie từ file"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

COOKIE = load_cookie(config.COOKIE_FILE)

def is_method_supported(status):
    if status in (405, 501):
        return False
    if config.STRICT_MODE:
        return 200 <= status < 400
    return True

def check_method(path):
    """
    Hàm test 1 endpoint xem support GET/POST hay không.
    Đồng thời test sự khác biệt khi thêm tham số (param) -> xem param có tác động không.
    """
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    results = {"GET": False, "POST": False}

    def body_sig(resp):
        return len(resp.content) if resp is not None else -1

    try:
        # --- GET ---
        r_get = requests.get(url, timeout=timeout, allow_redirects=False)
        h_get = body_sig(r_get)

        # Gửi GET kèm thêm param ảo để so sánh
        r_get_p = requests.get(url, params={"aaaa": "1"}, timeout=timeout, allow_redirects=False)
        h_get_p = body_sig(r_get_p)

        # Nếu status hợp lệ → endpoint support GET
        if is_method_supported(r_get.status_code):
            results["GET"] = True
            # results["GET_param"] = (h_get != h_get_p)

        # Nếu server trả header Allow
        allow_hdr = r_get.headers.get("Allow", "")
        if "GET" in allow_hdr.upper():
            results["GET"] = True

        # --- POST ---
        r_post = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            timeout=timeout,
            allow_redirects=False
        )
        h_post = body_sig(r_post)

        # POST có thêm param ảo
        r_post_p = requests.post(
            url,
            json={"aaaa": "1"},
            headers={"Content-Type": "application/json"},
            timeout=timeout,
            allow_redirects=False
        )
        h_post_p = body_sig(r_post_p)

        # Nếu status hợp lệ → endpoint support POST
        if is_method_supported(r_post.status_code):
            results["POST"] = True
            # results["POST_param"] = (h_post != h_post_p)

        # Nếu server trả header Allow
        allow_hdr_post = r_post.headers.get("Allow", "")
        if "POST" in allow_hdr_post.upper():
            results["POST"] = True

    except requests.RequestException as e:
        print(f"[!] Lỗi khi test {url}: {e}")

    return results

def main():
    get_endpoints = []
    post_endpoints = []

    # Đọc tất cả path từ file input
    with open(input_file) as f:
        paths = [line.strip() for line in f if line.strip()]

    for path in paths:
        print(f"[*] Đang test {path}")
        res = check_method(path)

        if res.get("GET"):
            get_endpoints.append(path)
        if res.get("POST"):
            post_endpoints.append(path)

    # Lưu kết quả ra file
    with open(get_file, "w") as f:
        f.write("\n".join(get_endpoints))
    with open(post_file, "w") as f:
        f.write("\n".join(post_endpoints))

    print(f"\n[+] Tổng kết:")
    print(f"GET endpoints: {len(get_endpoints)} -> {get_file}")
    print(f"POST endpoints: {len(post_endpoints)} -> {post_file}")

    # --- Chạy ffuf ---
    def run_ffuf(cmd):
    	subprocess.run(cmd)

    if get_endpoints:
        print("\n[+] Chạy ffuf cho GET ...")
        run_ffuf([
            "ffuf",
            "-w", config.PARAM_FILE + ":PARAM",
            "-w", get_file + ":PATH",
            "-u", f"{base_url}PATH?PARAM=1",
            "-mc", "200-400",
            "-v",
            "-t", "50",
            "-rate", "100",
            "-H", f"Cookie: {COOKIE}",
            "-o", config.FFUF_GET_JSON,
            "-of", "json"
        ])

    if post_endpoints:
        print("\n[+] Chạy ffuf cho POST ...")
        run_ffuf([
            "ffuf",
            "-w", config.PARAM_FILE + ":PARAM",
            "-w", post_file + ":PATH",
            "-u", f"{base_url}PATH",
            "-X", "POST",
            "-d", '{\"PARAM\": \"1\"}',
            "-H", "Content-Type: application/json",
            "-mc", "200-500",
            "-v",
            "-t", "50",
            "-rate", "100",
            "-H", f"Cookie: {COOKIE}",
            "-o", config.FFUF_POST_JSON,
            "-of", "json"
        ])

if __name__ == "__main__":
    main()

