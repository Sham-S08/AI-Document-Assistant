from langchain_chroma import Chroma
from app.embeddings import get_embeddings
from utils.config import CHROMA_DB_DIR


def create_vector_store(docs, collection_name):

    embeddings = get_embeddings()

    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=CHROMA_DB_DIR,
        collection_name=collection_name
    )

    return db
