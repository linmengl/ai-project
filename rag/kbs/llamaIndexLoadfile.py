from llama_index.llms.ollama import Ollama
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import gradio as gr
import os

# 禁用 tokenizer 并行加速避免告警
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 1. 初始化 LLM
Settings.llm = Ollama(
    model="llama3:8b",
    system_prompt="你是一个中文助手，请始终使用简体中文回答问题。",
    temperature=0.7)

# 2. 加载文档：支持 PDF、Word、Markdown
reader = SimpleDirectoryReader(
    input_dir="docs",
    required_exts=[".pdf", ".docx", ".md"]
)
documents = reader.load_data()

# embedding
embedding_model = HuggingFaceEmbedding(model_name="shibing624/text2vec-base-multilingual")

# 构建索引
index = VectorStoreIndex.from_documents(documents, embed_model=embedding_model)

# 持久化
index.storage_context.persist(persist_dir="./storage")

query_engine = index.as_query_engine()

def ask_question(query):
    retriever = index.as_retriever(similarity_top_k=20)
    nodes = retriever.retrieve(query)
    for i, node in enumerate(nodes):
        print(f"文档片段 {i + 1}:\n", node.text[:800])
    response = query_engine.query(query)
    return str(response)

gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(label="请输入你的问题"),
    outputs=gr.Textbox(label="回答"),
    title="📚 文档问答系统"
).launch(share=True)

