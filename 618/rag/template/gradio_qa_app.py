import gradio as gr
import os
import upload
import engine

# 禁用 tokenizer 并行加速避免告警
os.environ["TOKENIZERS_PARALLELISM"] = "false"

engine.init_llm()
engine.init_embedding()



def get_answer(tenant_id: str, question: str) -> str:
    """
    输入问题，返回文档问答结果。
    """
    try:
        print("✅ 用户提问"+question)
        response = engine.get_query_engine(tenant_id).query(question)
        return str(response)
    except Exception as e:
        return f"❌ 问答失败: {str(e)}"

# Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("# 📄 文档问答系统 (支持 PDF, Word, Markdown, TXT)")
    # 添加租户ID输入框
    tenant_id = gr.Textbox(label="租户ID", placeholder="请输入租户ID", type="text")

    with gr.Row():
        # 文件上传组件
        file_upload = gr.File(
            label="上传文档",
            file_types=[".pdf", ".docx", ".md", ".txt"],
            type="filepath",
            file_count="single"
            # file_count="multiple"
        )
        file_list = gr.DataFrame(
            headers=["文件名", "大小", "上传时间"],
            interactive=False,
            label="已上传文件"
        )
    upload_btn = gr.Button("上传并构建索引")
    upload_result = gr.Textbox(label="上传状态")
    upload_btn.click(upload.upload_file, inputs=[tenant_id, file_upload], outputs=upload_result)

    gr.Markdown("## 💬 开始提问")
    question = gr.Textbox(label="你的问题", placeholder="请问这个文档讲了什么？")
    answer = gr.Textbox(label="回答")
    ask_btn = gr.Button("提问")
    ask_btn.click(get_answer, inputs=[tenant_id, question], outputs=answer)

if __name__ == "__main__":
    demo.launch(share=True)
