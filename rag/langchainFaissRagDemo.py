from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PDFMinerLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama

loader = PDFMinerLoader("卓有成效的管理者_副本.pdf")
docs = loader.load()
print("1.文档加载完成")

# 文本切分
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)
# print("2.文档被切分成 "+{len(chunks)} +"个 chunks")
print("22")

embedding_model = HuggingFaceEmbeddings(model_name = "shibing624/text2vec-base-multilingual")
# embedding_model = HuggingFaceEmbeddings(model_name = "shibing624/text2vec-base-chinese")
# embedding_model = HuggingFaceEmbeddings(model_name = "./text2vec")

db = FAISS.from_documents(chunks, embedding_model)
print("3. 向量库构建完成")
retriever = db.as_retriever()
llm = Ollama(model="deepseek-r1:7b", temperature=0.7)

qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
print("4. QA链构建完成")

query="这个文件讲了什么？"
repose=qa.run(query=query)

print("5")
print(repose)