import os
from langchain_community.vectorstores.faiss import FAISS

from rag.embedder import get_embedding_model


BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "vectorstore")


def get_retriever():

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            "Vectorstore not found. Run build_vectorstore.py first."
        )

    embeddings = get_embedding_model()

    vectorstore = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )