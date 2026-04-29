from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import re
from PIL import Image
import io

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# テキスト判定
def analyze_text(text):
    sentences = text.split("。")
    avg_len = sum(len(s) for s in sentences) / max(len(sentences),1)
    repetition = len(re.findall(r'(..)\1{2,}', text))
    
    score = 0
    if avg_len > 40:
        score += 1
    if repetition > 0:
        score += 1

    return score

# 画像判定
def analyze_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    width, height = img.size
    
    score = 0
    if width % 2 == 0 and height % 2 == 0:
        score += 1

    return score

# API
@app.post("/analyze")
async def analyze(text: str = Form(""), file: UploadFile = File(None)):
    text_score = analyze_text(text) if text else 0
    image_score = 0

    if file:
        image_bytes = await file.read()
        image_score = analyze_image(image_bytes)

    total = text_score + image_score

    if total >= 2:
        result = "AIの可能性が高い"
    elif total == 1:
        result = "やや怪しい"
    else:
        result = "人間の可能性が高い"

    return {"result": result}

# 起動
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
