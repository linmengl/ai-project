from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import config
from llama_index.core import StorageContext, load_index_from_storage
import os
from llama_index.core.query_engine import BaseQueryEngine

# 禁用 tokenizer 并行加速避免告警
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 初始化 LLM 和 embedding
def init_llm():
    Settings.llm = Ollama(
        model=config.LLM_MODEL,
        system_prompt="你是一个中文助手，请始终使用简体中文回答问题。",
        temperature=0.7
    )

def init_embedding():
    embedding = HuggingFaceEmbedding(model_name=config.EMBEDDING_MODEL)
    Settings.embed_model = embedding


# 加载现有索引（优先使用已有的）
def load_or_build_index():
    if os.path.exists(os.path.join(config.INDEX_DIR, "index_store.json")):
        storage_context = StorageContext.from_defaults(persist_dir=config.INDEX_DIR)
        return load_index_from_storage(storage_context)
    return build_index()

# 上传接口
def do_upload_file(file):
    print(f"type of file: {type(file)}, value: {file}")
    filename = os.path.basename(file)
    print("上传文件：" + filename)
    file_write_path = os.path.join(config.UPLOAD_DIR, filename)
    print("文件写入路径："+file_write_path)
    # 以二进制只读模式打开上传文件（路径由 gr.File(..., type="filepath") 返回
    with open(file, "rb") as src, open(file_write_path, "wb") as dst:
        dst.write(src.read())

from typing import Dict
import config

_index_cache: Dict[str, BaseQueryEngine] = {}

def get_paths(tenant_id: str):
    upload_path = os.path.join(config.UPLOAD_DIR, tenant_id)
    index_path = os.path.join(config.INDEX_DIR, tenant_id)
    os.makedirs(upload_path, exist_ok=True)
    os.makedirs(index_path, exist_ok=True)
    return upload_path, index_path

# 构建索引（首次或更新文档后调用）
def build_index(tenant_id: str):
    upload_dir, index_dir = get_paths(tenant_id)
    docs = SimpleDirectoryReader(upload_dir).load_data()
    index = VectorStoreIndex.from_documents(docs)
    index.storage_context.persist(persist_dir=index_dir)
    _index_cache[tenant_id] = index.as_query_engine()

def get_query_engine(tenant_id: str):
    if tenant_id in _index_cache:
        return _index_cache[tenant_id]
    _, index_dir = get_paths(tenant_id)
    if os.path.exists(index_dir):
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        index = load_index_from_storage(storage_context)
        engine = index.as_query_engine()
        _index_cache[tenant_id] = engine
        return engine
    raise ValueError(f"Tenant '{tenant_id}' has no index. Please upload documents first.")