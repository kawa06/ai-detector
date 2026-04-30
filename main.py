from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import os

# ←これが無いとエラーになる
app = FastAPI()

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
    if text:
        result = "AIっぽい"
    else:
        result = "人間っぽい"

    return {"result": result}

# 起動
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
