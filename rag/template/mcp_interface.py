import engine

engine.init_llm()

def get_answer(question: str, tenant_id: str) -> str:
    """
    输入问题，返回文档问答结果。
    """
    try:
        query_engine = engine.get_query_engine(tenant_id=tenant_id).as_query_engine()
        response = query_engine.query(question)
        return str(response)
    except Exception as e:
        return f"❌ 问答失败: {str(e)}"


# 上传接口
def upload_file(files):
    for file in files:
        engine.do_upload_file(file)
    global doc_index, query_engine
    doc_index = engine.get_query_engine()
    query_engine = doc_index.as_query_engine()
    print("✅ 文件上传并更新索引成功")