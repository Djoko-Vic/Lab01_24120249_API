import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO
import uvicorn

# CẤU HÌNH MODEL
model_id = "prompthero/openjourney"

print("Đang tải mô hình, vui lòng đợi (có thể mất vài phút lần đầu)...")
print(f"  Model: {model_id}")

# Tự động chọn GPU nếu có, không thì dùng CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

print(f"  Thiết bị: {device.upper()}")
if device == "cpu":
    print("   Chạy trên CPU sẽ chậm hơn GPU (mỗi ảnh ~2-5 phút)")

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=dtype,
    safety_checker=None,        
    requires_safety_checker=False
)
pipe = pipe.to(device)

print("Tải mô hình thành công!\n")

# KHỞI TẠO FASTAPI
app = FastAPI(title="OpenJourney Text-to-Image API (Local)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str

# ENDPOINTS
@app.get("/")
async def root():
    return {
        "system": "OpenJourney Generation API",
        "description": "API này nhận văn bản đầu vào và sinh ra hình ảnh mang phong cách Midjourney v4.",
        "model_used": model_id,
        "device": device
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "gpu_available": torch.cuda.is_available(),
        "device": device
    }

@app.post("/generate")
async def generate_image(req: GenerateRequest):
    if not req.prompt or req.prompt.strip() == "":
        raise HTTPException(status_code=400, detail="Lỗi: Prompt không được để trống.")

    try:
        full_prompt = f"mdjrny-v4 style, {req.prompt}"
        print(f"Đang sinh ảnh cho prompt: '{req.prompt}'")

        image = pipe(full_prompt).images[0]

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        print("Sinh ảnh thành công!")
        return {
            "prompt_received": req.prompt,
            "status": "success",
            "image_base64": img_str
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống trong lúc sinh ảnh: {str(e)}")


# CHẠY SERVER
if __name__ == "__main__":
    print("   Khởi động server FastAPI tại http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   Nhấn Ctrl+C để dừng\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
