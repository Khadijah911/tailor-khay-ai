import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

knowledge_base = Path(r"C:\Users\USER\OneDrive\Desktop\AI_AGENT\agent_projects\Tailor_khay_ai\knowledge_base")
pdf_files = list(knowledge_base.glob("*.pdf"))
print(pdf_files)
all_documents = []


for pdf_file in pdf_files:
    file_loader = PyPDFLoader(pdf_file)
    file_docs = file_loader.load()

    for doc in file_docs:
        doc.metadata["source"] = pdf_file.stem.upper()

    all_documents.extend(file_docs)
print(len(all_documents))
print(all_documents[0].metadata)
print(all_documents[0].page_content[:300])

splitter=RecursiveCharacterTextSplitter(
    chunk_size=200,chunk_overlap=50
)
chunks=splitter.split_documents(all_documents)

print(f"Original documents: {len(all_documents)}")
print(f"Chunks created: {len(chunks)}")

print(chunks[0].page_content)
print(chunks[0].metadata)

emb = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=emb,
    persist_directory="./vector_store")
 

print("Vector database created successfully!")