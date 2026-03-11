from langchain_classic.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
Answer the question using the context below.

Context:
{context}

Question:
{question}

Answer clearly:
""",
    input_variables=["context", "question"]
)
