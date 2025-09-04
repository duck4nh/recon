import json
import config
from collections import defaultdict, Counter

def process_ffuf(input_file, output_file):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[!] Không tìm thấy {input_file}, bỏ qua")
        return

    results = data.get("results", [])
    method = data.get("config", {}).get("method", "UNKNOWN")

    endpoints = defaultdict(list)
    for r in results:
        path = r["input"]["PATH"]
        param = r["input"]["PARAM"]
        length = r["length"]
        endpoints[path].append((param, length))

    output = []
    for path, params in endpoints.items():
        lengths = [l for _, l in params]
        default_len = Counter(lengths).most_common(1)[0][0]
        diff_params = [p for p, l in params if l != default_len]
        if diff_params:
            output.append({
                "method": method,
                "endpoint": f"/{path}",
                "params": diff_params
            })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"[+] Xuất kết quả ra {output_file}")

def main():
    process_ffuf(config.FFUF_GET_WORDLIST_JSON, config.FINAL_GET_WORDLIST_JSON)
    process_ffuf(config.FFUF_POST_WORDLIST_JSON, config.FINAL_POST_WORDLIST_JSON)

if __name__ == "__main__":
    main()