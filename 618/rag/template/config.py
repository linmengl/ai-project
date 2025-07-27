import os

UPLOAD_DIR = "docs"
INDEX_DIR = "storage"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

LLM_MODEL = "llama3:8b"
EMBEDDING_MODEL = "shibing624/text2vec-base-multilingual"