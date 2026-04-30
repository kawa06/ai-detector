import re
from PIL import Image
import io

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

def analyze_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    width, height = img.size

    score = 0
    if width % 2 == 0 and height % 2 == 0:
        score += 1

    return score

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
