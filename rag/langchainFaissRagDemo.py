from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PDFMinerLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.llms import HuggingFaceHub
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

loader = PDFMinerLoader("金字塔原理大全集.pdf")
docs = loader.load()

print("1")
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)
print("2")
embedding_model = HuggingFaceEmbeddings(model_name = "shibing624/text2vec-base-chinese")

db = FAISS.from_documents(chunks, embedding_model)
print("3")
retriever = db.as_retriever()
llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature":0.7})
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
print("4")
query="这个文件讲了什么？"
repose=qa.run(query=query)
print("5")
print(repose)