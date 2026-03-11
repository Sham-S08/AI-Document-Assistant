from langchain_chroma import Chroma
from app.embeddings import get_embeddings
from utils.config import CHROMA_DB_DIR


def get_retriever(collection_name):

    embeddings = get_embeddings()

    db = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings,
        collection_name=collection_name
    )

    retriever = db.as_retriever()

    return retriever
