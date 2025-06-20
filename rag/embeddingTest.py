import math
from sentence_transformers import SentenceTransformer

def dot_product(a, b):
    return sum(x*y for x, y in zip(a, b))

def norm(v):
    return math.sqrt(sum(x*x for x in v))

def cosine_similarity(a, b):
    return dot_product(a, b) / (norm(a) * norm(b))

vec1 = [1, 2, 3]
vec2 = [4, 5, 6]
print("66")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
print("77")
sent1 = "I like machine learning."
sent2 = "I enjoy studying AI."

emb1 = model.encode(sent1)

print(emb1.shape)
emb2 = model.encode(sent2)

similarity = cosine_similarity(emb1, emb2)
print("99999")
print(f"相似度：{similarity:.4f}")