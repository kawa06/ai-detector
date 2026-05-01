import os

UPLOAD_DIR = "uploads"

# =========================
# フォルダ安全作成（重要）
# =========================
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# =========================
# 画像スコア判定
# =========================
def fake_image_score(filename: str):

    score = 50

    # ファイル形式で軽く判定
    if filename.endswith(".png"):
        score += 10

    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        score += 5

    # 上限調整
    if score > 100:
        score = 100

    if score < 0:
        score = 0

    return score


# =========================
# （必要なら保存用関数）
# =========================
def save_file(file, path: str):
    with open(path, "wb") as f:
        f.write(file)
