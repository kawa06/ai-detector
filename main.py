from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

# ← これが超重要
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

# 判定API
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
