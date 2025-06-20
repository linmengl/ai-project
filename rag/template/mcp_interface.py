import engine

engine.init_llm()
engine.init_embedding()
# 全局只初始化一次
doc_index = engine.load_or_build_index()
query_engine = doc_index.as_query_engine()

def get_answer(question: str) -> str:
    """
    输入问题，返回文档问答结果。
    """
    try:
        response = query_engine.query(question)
        return str(response)
    except Exception as e:
        return f"❌ 问答失败: {str(e)}"


# 上传接口
def upload_file(files):
    for file in files:
        engine.do_upload_file(file)
    global doc_index, query_engine
    doc_index = engine.build_index()
    query_engine = doc_index.as_query_engine()
    print("✅ 文件上传并更新索引成功")