from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


documents = SimpleDirectoryReader("data/").load_data()

# embedding = HuggingFaceEmbedding(model_name = "moka-ai/m3e-base")
# embedding = HuggingFaceEmbedding(model_name = "shibing624/text2vec-base-multilingual")
embedding = HuggingFaceEmbedding(model_name = "./text2vec")

index = VectorStoreIndex.from_documents(documents, embed_model = embedding)

query_engine = index.as_query_engine()

response = query_engine.query("介绍一下这个文档的内容")
print(response)