from langchain_core.tools import tool
from langchain.llms import LlamaCpp

@tool("add", return_direct=True)
def add(a: int, b: int) -> int:
    return a + b

llm = LlamaCpp(model_path="llama3-70b.gguf", n_ctx=4096, temperature=0)
llm_with_tools = llm.bind_tools([add])

resp = llm_with_tools.invoke("55 + 66 等于多少？")
print(resp.content)  # 正常会打印 "121"