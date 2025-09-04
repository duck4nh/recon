# main.py
import katana
import ffuf
import end

def main():
    print("\n=== Bước 1: Chạy Katana ===")
    katana.main()

    print("\n=== Bước 2: Chạy FFUF ===")
    ffuf.main()

    print("\n=== Bước 3: Chuẩn hóa kết quả ===")
    end.main()

if __name__ == "__main__":
    main()
