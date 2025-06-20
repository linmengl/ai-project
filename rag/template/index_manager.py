# index_manager.py
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.base import BaseQueryEngine
from typing import Dict
import config

_index_cache: Dict[str, BaseQueryEngine] = {}

def get_paths(tenant_id: str):
    upload_path = os.path.join(config.UPLOAD_DIR, tenant_id)
    index_path = os.path.join(config.INDEX_DIR, tenant_id)
    os.makedirs(upload_path, exist_ok=True)
    os.makedirs(index_path, exist_ok=True)
    return upload_path, index_path

def build_index_for_tenant(tenant_id: str):
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