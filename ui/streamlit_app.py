import sys
import os

# Maintain your existing path logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.rag_pipeline import create_rag
from loaders.pdf_loader import load_pdf
from text_splitters.splitter import split_documents
from vectorstore.chroma_store import create_vector_store

# --- Page Config ---
st.set_page_config(page_title="AI Document Assistant", page_icon="📄", layout="wide")

# --- Custom CSS for Professional Look ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    .source-box { background-color: #7eb2e6; padding: 10px; border-radius: 5px; font-size: 0.85rem; border-left: 4px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar: Project Info & Navigation ---
with st.sidebar:
    st.title("Navigation")
    st.markdown("### Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", help="Upload a document to start the AI analysis")
    
    st.divider()
    
    st.markdown("### System Information")
    with st.expander("Tech Stack Details", expanded=True):
        st.write("- **Framework:** LangChain")
        st.write("- **Database:** Chroma DB")
        st.write("- **LLM:** Groq")
        st.write("- **Embeddings:** HuggingFace")

    st.divider()
    st.info("This application uses Retrieval-Augmented Generation (RAG) to provide context-aware answers from your private documents.")

# --- Main Header Section ---
st.header("AI Document Assistant")
st.caption("Upload documents and instantly extract insights using AI.")

# --- Processing Logic ---
if uploaded_file:
    # Ensure data directory exists
    os.makedirs("data/documents", exist_ok=True)
    file_path = f"data/documents/{uploaded_file.name}"
    collection_name = uploaded_file.name.replace(".pdf", "")

    # Check if we need to process (avoid re-processing if already in session)
    if "current_doc" not in st.session_state or st.session_state.current_doc != uploaded_file.name:
        with st.status("Indexing document...", expanded=True) as status:
            st.write("Saving file...")
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.write("Loading PDF content...")
            docs = load_pdf(file_path)
            
            st.write("Splitting text into chunks...")
            chunks = split_documents(docs)
            
            st.write("Generating embeddings and storage...")
            create_vector_store(chunks, collection_name)
            
            st.session_state.current_doc = uploaded_file.name
            status.update(label="Document indexed successfully!", state="complete", expanded=False)

    # --- Chat / Question Interface ---
    st.divider()
    
    # Initialize chat history if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                with st.expander("View Sources"):
                    for src in message["sources"]:
                        st.markdown(f"<div class='source-box'>{src}</div>", unsafe_allow_html=True)

    # User Input
    if question := st.chat_input("Ask a question about your document"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})

        # Generate AI Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                qa = create_rag(collection_name)
                result = qa.invoke({"query": question})
                answer = result["result"]
                sources = [str(doc.metadata) for doc in result["source_documents"]]
                
                st.markdown(answer)
                with st.expander("View Sources"):
                    for src in sources:
                        st.markdown(f"<div class='source-box'>{src}</div>", unsafe_allow_html=True)
                
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer, 
                    "sources": sources
                })

else:
    # Placeholder when no file is uploaded
    st.info("Please upload a PDF document in the sidebar to begin.")
    
    # Feature explanation tiles
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 1. Upload")
        st.write("Upload any PDF document to the secure local storage.")
    with col2:
        st.markdown("#### 2. Index")
        st.write("The AI creates a semantic map of your document content.")
    with col3:
        st.markdown("#### 3. Ask")
        st.write("Get instant, cited answers to complex questions.")

# --- Footer / About Section ---
st.divider()
with st.expander("About This Project"):
    st.write("""
        This application demonstrates a full **RAG (Retrieval Augmented Generation)** pipeline. 
        It performs document semantic search by converting text into vector embeddings, 
        storing them in a vector database, and retrieving relevant context to ground 
        the LLM's responses, minimizing hallucinations.
    """)