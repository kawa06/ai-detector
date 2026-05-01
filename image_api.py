from fastapi import APIRouter, UploadFile, File
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 🧠 画像AI判定（簡易版）
def fake_image_score(filename: str):
    score = 50

    if filename.endswith(".png"):
        score += 10
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        score += 5

    return min(100, score)


# 📸 画像アップロード＆判定
@router.post("/image-predict")
async def image_predict(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id + "_" + file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    score = fake_image_score(file.filename)

    result = "AI生成の可能性あり" if score >= 60 else "人間または自然画像"

    return {
        "filename": file.filename,
        "score": score,
        "result": result
    }

def fake_image_score(filename: str):

    score = 50

    if filename.endswith(".png"):
        score += 10

    if filename.endswith(".jpg"):
        score += 5

    if score > 100:
        score = 100

    return score
