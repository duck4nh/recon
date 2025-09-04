import katana2
import ffuf2
import end2

def main():
    print("=== Phase 2: Fuzz endpoint bằng wordlist ===")
    katana2.main()

    print("=== Phase 2: Fuzz tham số trên endpoint tìm được ===")
    ffuf2.main()

    print("=== Phase 2: Xử lý kết quả ===")
    end2.main()

if __name__ == "__main__":
    main()