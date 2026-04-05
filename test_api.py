import requests
import base64
import os
import json
from datetime import datetime

# URL server
API_URL = "http://localhost:8000"

def test_api():
    print("=" * 50)
    print("TEST OPENJOURNEY API LOCAL")
    print("=" * 50)

    # ---- 0. Thông tin API ----
    print("\n0. Kiểm tra GET / (Thông tin API):")
    try:
        resp = requests.get(f"{API_URL}/", timeout=10)
        print(resp.json())
    except Exception as e:
        print(f" Lỗi: {e}")
        print(" Hãy chắc chắn api_local.py đang chạy!")
        return

    print("-" * 30)

    # ---- 1. Kiểm tra health ----
    print("\n1. Kiểm tra /health:")
    resp_health = requests.get(f"{API_URL}/health", timeout=10)
    print(resp_health.json())

    # ---- 2. Sinh ảnh ----
    print("\n2. Gửi request sinh ảnh tới /generate...")
    print("   (Trên CPU có thể mất 2-5 phút, hãy kiên nhẫn!)")
    prompt = input("Nhập prompt: ")
    payload = {"prompt": prompt}

    try:
        response = requests.post(
            f"{API_URL}/generate",
            json=payload,
            timeout=600
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ API trả kết quả thành công!")

            # Lưu ảnh ra file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            img_data = base64.b64decode(data["image_base64"])
            filename = f"generated_{timestamp}.png"
            filepath = os.path.join(os.path.dirname(__file__), filename)

            with open(filepath, "wb") as f:
                f.write(img_data)

            print(f"Ảnh đã được lưu tại: {filepath}")

            # Lưu toàn bộ JSON response ra file
            json_filename = f"generated_{timestamp}.json"
            json_filepath = os.path.join(os.path.dirname(__file__), json_filename)

            with open(json_filepath, "w", encoding="utf-8") as jf:
                json.dump(data, jf, ensure_ascii=False, indent=2)

            print(f"JSON đã được lưu tại: {json_filepath}")
        else:
            print(f"Gọi API thất bại. Mã lỗi: {response.status_code}")
            print(response.text)

    except requests.exceptions.Timeout:
        print("⏱Timeout!")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    test_api()
