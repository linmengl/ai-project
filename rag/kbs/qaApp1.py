import os
import gradio as gr
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

UPLOAD_DIR = "docs"
INDEX_DIR = "storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 禁用 tokenizer 并行加速避免告警
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 1. 初始化 LLM
Settings.llm = Ollama(
    model="llama3:8b",
    system_prompt="你是一个中文助手，请始终使用简体中文回答问题。",
    temperature=0.7)

embedding = HuggingFaceEmbedding(model_name="shibing624/text2vec-base-multilingual")

# 文档处理逻辑
def build_index():
    documents = SimpleDirectoryReader(UPLOAD_DIR).load_data()
    print("Building index...")
    index = VectorStoreIndex.from_documents(documents, embed_model = embedding)
    index.storage_context.persist(persist_dir=INDEX_DIR)
    return index

# 构建索引缓存
doc_index = build_index()
query_engine = doc_index.as_query_engine()

# 问答接口
def ask_question(question):
    # retriever = doc_index.as_retriever(similarity_top_k=20)
    # nodes = retriever.retrieve(question)
    # for i, node in enumerate(nodes):
    #     print(f"文档片段 {i + 1}:\n", node.text[:800])
    response = query_engine.query(question)
    return str(response)


# 上传接口
def upload_file(files):
    for file in files:
        print(f"type of file: {type(file)}, value: {file}")
        filename = os.path.basename(file)
        print("上传文件：" + filename)
        file_write_path = os.path.join(UPLOAD_DIR, filename)
        print("文件写入路径："+file_write_path)
        # 以二进制只读模式打开上传文件（路径由 gr.File(..., type="filepath") 返回
        with open(file, "rb") as src, open(file_write_path, "wb") as dst:
            dst.write(src.read())
    global doc_index, query_engine
    doc_index = build_index()
    query_engine = doc_index.as_query_engine()
    print("✅ 文件上传并更新索引成功")

# Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("# 📄 文档问答系统 (支持 PDF, Word, Markdown, TXT)")

    with gr.Row():
        # 文件上传组件
        file_upload = gr.File(
            label="上传文档",
            file_types=[".pdf", ".docx", ".md", ".txt"],
            type="filepath",
            file_count="multiple"
        )
    upload_btn = gr.Button("上传并构建索引")
    upload_result = gr.Textbox(label="上传状态")
    upload_btn.click(upload_file, inputs=file_upload, outputs=upload_result)

    gr.Markdown("## 💬 开始提问")
    question = gr.Textbox(label="你的问题", placeholder="请问这个文档讲了什么？")
    answer = gr.Textbox(label="回答")
    ask_btn = gr.Button("提问")
    ask_btn.click(ask_question, inputs=question, outputs=answer)

if __name__ == "__main__":
    demo.launch(share=True)

