from langchain_openai import OpenAIEmbeddings ,ChatOpenAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

emb = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)


vectorstore = Chroma(
    persist_directory="./vector_store",
    embedding_function=emb
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 10
    }
)
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=api_key)

def answer_business_question(question: str):
    docs=retriever.invoke(question)
    context="\n\n".join(doc.page_content for doc in docs)
    prompt = f"""
    You are Tailor Khay's business assistant.

    Answer the customer's question ONLY using the information below.

    If the answer cannot be found in the knowledge base, say you don't know instead of making something up.

    Knowledge Base:
    {context}

    Customer Question:
    {question}
    """
    

    response=llm.invoke(prompt)
    return response.content



