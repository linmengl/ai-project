import os
from typing import Dict

from llama_index.core import Settings
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

import config
import upload

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



def get_query_engine(tenant_id: str):
    if tenant_id in _index_cache:
        return _index_cache[tenant_id]
    _, index_dir = upload.get_paths(tenant_id)
    if os.path.exists(index_dir):
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        index = load_index_from_storage(storage_context)
        engine = index.as_query_engine()
        _index_cache[tenant_id] = engine
        return engine
    raise ValueError(f"Tenant '{tenant_id}' has no index. Please upload documents first.")

_index_cache: Dict[str, BaseQueryEngine] = {}

# 构建索引（首次或更新文档后调用）
def build_index(tenant_id: str):
    upload_dir, index_dir = upload.get_paths(tenant_id)

    docs = SimpleDirectoryReader(upload_dir).load_data()
    index = VectorStoreIndex.from_documents(docs)
    index.storage_context.persist(persist_dir=index_dir)
    _index_cache[tenant_id] = index.as_query_engine()