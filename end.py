import json
import os
from collections import defaultdict, Counter
import config

def process_ffuf(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"\n[!] Bỏ qua vì không tìm thấy {input_file}")
        return
    with open(input_file, "r") as f:
        data = json.load(f)

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
            output.append({"method": method, "endpoint": f"{path}", "params": diff_params})

    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[+] Đã xử lý {input_file} → {output_file}")

def main():
    process_ffuf(config.FFUF_GET_JSON, config.GET_JSON)
    process_ffuf(config.FFUF_POST_JSON, config.POST_JSON)

if __name__ == "__main__":
    main()
