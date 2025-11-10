from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from .config import settings

def get_embeddings():
    return OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

def get_vectorstore(persist_directory: str = None):
    persist_directory = persist_directory or settings.chroma_persist_directory
    embeddings = get_embeddings()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vectordb

def build_qa_chain():
    model = ChatOpenAI(openai_api_key=settings.openai_api_key, model=settings.model_name, temperature=0.0)
    vectordb = get_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=retriever, return_source_documents=True)
    return qa
