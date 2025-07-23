import engine

engine.init_llm()

def get_answer(question: str, tenant_id: str) -> str:
    """
    输入问题，返回文档问答结果。
    """
    try:
        response = engine.get_query_engine(tenant_id).query(question)
        return str(response)
    except Exception as e:
        return f"❌ 问答失败: {str(e)}"


# 上传接口
def upload_file(tenant_id, files):
    for file in files:
        engine.do_upload_file(file, tenant_id)
    engine.build_index(tenant_id)
    print("✅ 文件上传并更新索引成功")