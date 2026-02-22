from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Returns embedding model.
    You can swap this later with OpenAI or other embedding providers.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )   