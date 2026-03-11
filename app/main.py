from app.rag_pipeline import create_rag

qa = create_rag()

while True:

    question = input("Ask: ")

    if question == "exit":
        break

    response = qa.invoke({"query": question})["result"]

    print("\nAnswer:", response)
