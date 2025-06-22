import gradio as gr
import mcp_interface as mci
from mcp_interface import get_answer
import os

# 禁用 tokenizer 并行加速避免告警
os.environ["TOKENIZERS_PARALLELISM"] = "false"
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
    upload_btn.click(mci.upload_file, inputs=file_upload, outputs=upload_result)

    gr.Markdown("## 💬 开始提问")
    question = gr.Textbox(label="你的问题", placeholder="请问这个文档讲了什么？")
    answer = gr.Textbox(label="回答")
    ask_btn = gr.Button("提问")
    ask_btn.click(get_answer, inputs=question, outputs=answer)

if __name__ == "__main__":
    demo.launch(share=True)
