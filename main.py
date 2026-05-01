from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import os
import re

from image_api import fake_image_score

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# テキスト判定
# =========================
def analyze_text(text: str):
    score = 0
    reasons = []

    if len(text) > 100:
        score += 1
        reasons.append("文章が長い")

    if text.count("。") > 3:
        score += 1
        reasons.append("文が多い")

    if re.search(r'(..)\1{2,}', text):
        score += 1
        reasons.append("繰り返し表現")

    if text.count("です") > 3:
        score += 1
        reasons.append("語尾が単調")

    return score, reasons

# =========================
# 簡易AI判定（ダミー）
# =========================
def ai_judge(text: str):
    return "AIの可能性が高い（AI判定）"

# =========================
# HTML表示
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/privacy.html", response_class=HTMLResponse)
def privacy():
    with open("privacy.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/terms.html", response_class=HTMLResponse)
def terms():
    with open("terms.html", "r", encoding="utf-8") as f:
        return f.read()

# =========================
# メインAPI（統合）
# =========================
@app.post("/analyze")
async def analyze(text: str = Form(""), file: UploadFile = File(None)):

    # 📸 画像がある場合
    if file:
        score = fake_image_score(file.filename)

        return {
            "type": "image",
            "score": score,
            "result": "画像解析結果"
        }

    # ❌ テキストなし
    if not text:
        return {"result": "入力してください"}

    # 🧠 テキスト判定
    score, reasons = analyze_text(text)

    if score >= 3:
        result = "AIの可能性が高い"
    elif score <= 1:
        result = "人間の可能性が高い"
    else:
        result = ai_judge(text)

    return {
        "type": "text",
        "score": score,
        "result": result,
        "reasons": reasons
    }

# =========================
# 起動
# =========================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
