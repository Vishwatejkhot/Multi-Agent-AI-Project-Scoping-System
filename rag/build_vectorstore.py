import os
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.embedder import get_embedding_model


BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "knowledge_base")
DB_PATH = os.path.join(BASE_DIR, "vectorstore")


def build_vectorstore():

    documents = []

    
    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(DATA_PATH, file))
            documents.extend(loader.load())

    if not documents:
        raise ValueError("No knowledge base files found.")

  
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    split_docs = splitter.split_documents(documents)

    
    embeddings = get_embedding_model()

    
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    
    vectorstore.save_local(DB_PATH)

    print("✅ Vector store created successfully at:", DB_PATH)


if __name__ == "__main__":
    build_vectorstore()