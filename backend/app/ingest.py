from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader, UnstructuredPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .config import settings
from typing import List
import os

def _loader_for_file(path: str):
    # support common types - add more loaders as needed
    if path.lower().endswith(".pdf"):
        return UnstructuredPDFLoader(path)
    return TextLoader(path, encoding="utf8")

def ingest_files(file_paths: List[str], persist_directory: str = None):
    persist_directory = persist_directory or settings.chroma_persist_directory
    docs = []
    for p in file_paths:
        loader = _loader_for_file(p)
        docs.extend(loader.load())
    # splitter
    splitter = CharacterTextSplitter(chunk_size=900, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    vectordb = Chroma.from_documents(documents=split_docs, embedding=embeddings, persist_directory=persist_directory)
    vectordb.persist()
    return len(split_docs)
