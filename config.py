# config.py

# ----------- Phase 1 -----------
# URL mục tiêu
URL = "http://10.3.2.52:3000"

# Cookie (nếu cần)
COOKIE_FILE = "/home/duck4nh/Desktop/cookie.txt"

# File tạm & output cho Katana
INPUT_FILE = "./results/input.txt"
OUTPUT_FILE = "./results/paths.txt"

# File kết quả phân loại method
GET_FILE = "./results/get_endpoints.txt"
POST_FILE = "./results/post_endpoints.txt"

# File kết quả fuzz của ffuf
FFUF_GET_JSON = "./results/ffuf_get.json"
FFUF_POST_JSON = "./results/ffuf_post.json"

# File kết quả chuẩn hóa
GET_JSON = "./results/get.json"
POST_JSON = "./results/post.json"

# Wordlist param
PARAM_FILE = "./param.txt"

# Timeout request (cho ffuf.py check_method)
TIMEOUT = 8

# Strict mode: True = chỉ tính 2xx/3xx, False = bỏ qua 405 & 501
STRICT_MODE = False

# ----------- Phase 2 -----------
WORDLIST = "./common.txt"   # wordlist brute force
OUTPUT_FILE_WORDLIST = "./results/paths_wordlist.json"
PATH_FILE_WORDLIST = "./results/paths_wordlist.txt"

# File kết quả phân loại method
GET_FILE_WORDLIST = "./results/get_endpoints_wordlist.txt"
POST_FILE_WORDLIST = "./results/post_endpoints_wordlist.txt"

# File kết quả fuzz tham số
FFUF_GET_WORDLIST_JSON = "./results/ffuf_get_wordlist.json"
FFUF_POST_WORDLIST_JSON = "./results/ffuf_post_wordlist.json"

# File kết quả chuẩn hóa cuối
FINAL_GET_WORDLIST_JSON = "./results/get_wordlist.json"
FINAL_POST_WORDLIST_JSON = "./results/post_wordlist.json"
