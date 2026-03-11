import os
from loaders.pdf_loader import load_pdf
from text_splitters.splitter import split_documents
from vectorstore.chroma_store import create_vector_store
from utils.config import DATA_PATH


def ingest():

    all_docs = []

    for file in os.listdir(DATA_PATH):

        if file.endswith(".pdf"):

            path = os.path.join(DATA_PATH, file)

            docs = load_pdf(path)

            all_docs.extend(docs)

    chunks = split_documents(all_docs)

    create_vector_store(chunks)

    print("Documents successfully indexed!")


if __name__ == "__main__":
    ingest()
