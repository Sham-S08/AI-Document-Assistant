from langchain_classic.chains import RetrievalQA
from langchain_groq import ChatGroq
from app.retriever import get_retriever
from app.prompts import prompt
from utils.config import MODEL_NAME


def create_rag(collection_name):

    llm = ChatGroq(
        model_name=MODEL_NAME,
        temperature=0
    )

    retriever = get_retriever(collection_name)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain
