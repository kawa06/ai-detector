from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from openai import OpenAI
import uvicorn
import os
import re

app = FastAPI()

# CORS設定（フロントと通信するため）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIキー
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# 自作判定
# =========================
def analyze_text(text):
    score = 0
    reasons = []

    if len(text) > 100:
        score += 1
        reasons.append("文章が長い")

    if text.count("。") > 3:
        score += 1
        reasons.append("文の数が多い")

    if re.search(r'(..)\1{2,}', text):
        score += 1
        reasons.append("同じ表現の繰り返し")

    if text.count("です") > 3:
        score += 1
        reasons.append("語尾が単調")

    return score, reasons

# =========================
# AI判定
# =========================
def ai_judge(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "この文章がAI生成か人間かを判定し、理由も短く答えてください"},
            {"role": "user", "content": text}
        ]
    )

    return response.choices[0].message.content

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
# 判定API
# =========================
@app.post("/analyze")
async def analyze(text: str = Form(""), file: UploadFile = File(None)):

    if not text:
        return {"result": "入力してください"}

    score, reasons = analyze_text(text)

    # 明確な場合（高速）
    if score >= 3:
        result = "AIの可能性が高い"

    elif score <= 1:
        result = "人間の可能性が高い"

    else:
        # あいまいな時だけAI
        ai_result = ai_judge(text)
        return {"result": ai_result}

    # 理由追加
    if reasons:
        result += "\n理由：" + "、".join(reasons)

    return {"result": result}



# ローカル起動用
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

@app.post("/predict")
def predict(data: TextIn):

    score = fake_ai_score(data.text)

    if score >= 60:
        result = "AIの可能性が高い"
    else:
        result = "人間の可能性が高い"

    return {
        "score": score,
        "result": result
    }
