from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # 显式禁用并行

from llama_index.llms.ollama import Ollama
Settings.llm = Ollama(
    # model="llama3:8b",
    model="deepseek-r1:7b",
    # system_prompt="你是一个中文助手，请始终使用简体中文回答问题。",
    temperature=0.7
)

documents = SimpleDirectoryReader("data/").load_data()

# embedding = HuggingFaceEmbedding(model_name = "moka-ai/m3e-base")
embedding = HuggingFaceEmbedding(model_name = "shibing624/text2vec-base-multilingual")
# embedding = HuggingFaceEmbedding(model_name = "./text2vec")

index = VectorStoreIndex.from_documents(documents, embed_model = embedding)

retriever = index.as_retriever(similarity_top_k=20)
nodes = retriever.retrieve("介绍一下这个文档的内容")
for i, node in enumerate(nodes):
    print(f"文档片段 {i+1}:\n", node.text[:800])


query_engine = index.as_query_engine()
response = query_engine.query("介绍一下这个文档的内容")
print(response)