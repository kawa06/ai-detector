from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from openai import OpenAI
import uvicorn
import os
import re

# ← ここで初めて使う
app = FastAPI()

# APIキー
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ←これが無いとエラーになる
app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# トップページ

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# 判定API（とりあえず簡易）

@app.post("/analyze")
async def analyze(text: str = Form(""), file: UploadFile = File(None)):

    if not text:
        return {"result": "入力してください"}

    score, reasons = analyze_text(text)

    if score >= 3:
        result = "AIの可能性が高い"
        
if score >= 3:
    result = "AIの可能性が高い"
elif score <= 1:
    result = "人間の可能性が高い"
else:
    # 条件を厳しくする
    if len(text) < 200:
        result = "人間の可能性が高い"
    else:
        ai_result = ai_judge(text)
        return {"result": ai_result}
        
        ai_result = ai_judge(text)
        return {"result": ai_result}

    if reasons:
        result += "\n理由：" + "、".join(reasons)

    return {"result": result}
    
@app.post("/analyze")
async def analyze(text: str = Form(""), file: UploadFile = File(None)):

    # 入力チェック
    if not text:
        return {"result": "入力してください"}

    # 自作判定
    score, reasons = analyze_text(text)

    # ■ 判定分岐
    if score >= 3:
        result = "AIの可能性が高い"

    elif score <= 1:
        result = "人間の可能性が高い"

    else:
        # ←ここが③（AI使う場所）
        ai_result = ai_judge(text)
        return {"result": ai_result}

    # 理由追加
    if reasons:
        result += "\n理由：" + "、".join(reasons)

    return {"result": result}
    
# 起動
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
    import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from fastapi.responses import HTMLResponse

@app.get("/privacy.html", response_class=HTMLResponse)
def privacy():
    with open("privacy.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/terms.html", response_class=HTMLResponse)
def terms():
    with open("terms.html", "r", encoding="utf-8") as f:
        return f.read()
