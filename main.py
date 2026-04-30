import re
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def cheap_analyze(text):
    score = 0

    # 文の長さ
    if len(text) > 100:
        score += 1

    # 文体の単調さ
    if text.count("。") > 3:
        score += 1

    # 繰り返し
    if re.search(r'(..)\1{2,}', text):
        score += 1

    return score


@app.post("/analyze")
async def analyze(text: str = Form(""), file: UploadFile = File(None)):

    if not text:
        return {"result": "入力してください"}

    score = cheap_analyze(text)

    # ■ ここが重要（分岐）
    if score == 0:
        return {"result": "人間の可能性が高い（簡易判定）"}

    if score >= 2:
        return {"result": "AIの可能性が高い（簡易判定）"}

    # ■ ここだけAI使う（約10〜20%だけ）
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "AI生成か人間かを判定してください。短く答えてください。"},
            {"role": "user", "content": text}
        ]
    )

    result = response.choices[0].message.content

    return {"result": result}
# 語尾パターン
if text.count("です") > 3:
    score += 1

# 同じ長さの文が続く
sentences = text.split("。")
lengths = [len(s) for s in sentences if s]
if len(set(lengths)) < 3:
    score += 1
