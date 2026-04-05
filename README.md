# OpenJourney Local API

> **Bài Thực Hành 1 - Application Programming Interface**
> Môn: Computational Thinking — Đại học Khoa Học Tự Nhiên TP.HCM

---

## Thông Tin Sinh Viên

| Thông tin     | Chi tiết                             |
|---------------|--------------------------------------|
| **Họ và tên** | Võ Nguyễn Việt Hoàng                |
| **MSSV**      | 24120249                             |
| **Môn học**   | Computational Thinking               |

---

## Mô Hình

**Tên mô hình:** `prompthero/openjourney`

🔗 **Liên kết Hugging Face:** [https://huggingface.co/prompthero/openjourney](https://huggingface.co/prompthero/openjourney)

OpenJourney là mô hình Stable Diffusion được fine-tune bởi [PromptHero](https://prompthero.com), có khả năng sinh ảnh theo phong cách **Midjourney v4** từ mô tả văn bản (text-to-image). Mô hình được huấn luyện trên hàng nghìn ảnh Midjourney chất lượng cao.

---

## Mô Tả Chức Năng

Dự án này triển khai mô hình `prompthero/openjourney` thành một **REST API** sử dụng **FastAPI**, cho phép:

| Endpoint | Phương thức | Chức năng |
|----------|-------------|-----------|
| `/` | `GET` | Xem thông tin API và mô hình đang dùng |
| `/health` | `GET` | Kiểm tra trạng thái server và GPU |
| `/generate` | `POST` | Nhận prompt văn bản → Trả về ảnh (base64) và file JSON |

**Luồng hoạt động:**
```
[Client] --POST /generate--> [FastAPI Server] --pipe()--> [OpenJourney Model]
                                                                   |
[Client] <-- JSON { image_base64 } <---------- [PIL Image → base64]
```

---

## Hướng Dẫn Cài Đặt
### Bước 1 — Clone hoặc tải thư mục dự án

```bash
git clone <repository-url>
cd Lab_1
```

### Bước 2 — Tạo môi trường ảo (khuyến nghị)
```bash
python -m venv venv
```
# Windows
```bash
venv\Scripts\activate
```
# macOS / Linux
```bash
source venv/bin/activate
```

### Bước 3 — Cài đặt thư viện
```bash
pip install -r requirements.txt
```
> ⏳ Lần đầu cài có thể mất 5–15 phút tùy kết nối mạng.

---

## Hướng Dẫn Chạy Chương Trình

### Khởi Động Server
```bash
python api_local.py
```
### Chạy File Test

Mở terminal **thứ hai**:

python test_api.py

Ảnh sinh ra sẽ được lưu tại cùng thư mục với tên `generated_YYYYMMDD_HHMMSS.png`.


### `GET /` — Thông tin API

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "system": "OpenJourney Generation API",
  "description": "API này nhận văn bản đầu vào và sinh ra hình ảnh mang phong cách Midjourney v4.",
  "model_used": "prompthero/openjourney",
  "device": "cpu"
}
```

---

### `GET /health` — Kiểm tra trạng thái

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "gpu_available": false,
  "device": "cpu"
}
```

---

### `POST /generate` — Sinh ảnh từ văn bản

**Sử dụng `curl`:**
```bash
curl -X POST http://localhost:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Beautiful night street in Japan"}'
```

**Sử dụng Python (`requests`):**
```python
import requests
import base64

response = requests.post(
    "http://localhost:8000/generate",
    json={"prompt": "A futuristic city in the clouds"},
    timeout=600
)

data = response.json()
img_data = base64.b64decode(data["image_base64"])

with open("output.png", "wb") as f:
    f.write(img_data)
print("Ảnh đã lưu: output.png")
```

**Body (JSON):**
```json
{
  "prompt": "Beautiful night street in Japan"
}
```

**Response:**
```json
{
  "prompt_received": "Beautiful night street in Japan",
  "status": "success",
  "image_base64": "iVBORw0KGgoAAAANSUhEUg..."
}
```

---

## Video Demo

[![Video Demo API OpenJourney](https://img.youtube.com/vi/3re1u9y-UOo/maxresdefault.jpg)](https://youtu.be/3re1u9y-UOo)

---
