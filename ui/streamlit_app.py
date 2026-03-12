import sys
import os

# Maintain your existing path logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.rag_pipeline import create_rag
from loaders.pdf_loader import load_pdf
from text_splitters.splitter import split_documents
from vectorstore.chroma_store import create_vector_store
import base64

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64("ui/bg.png")

# --- Page Config ---
st.set_page_config(page_title="AI Document Assistant", page_icon="📄", layout="wide")

# --- Custom CSS for Professional Look ---
st.markdown(f"""
<style>

/* ---------- GOOGLE FONTS IMPORT ---------- */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ---------- CSS VARIABLES ---------- */
:root {{
    --bg-deep:        #050a14;
    --bg-surface:     #0b1526;
    --bg-card:        rgba(13, 22, 44, 0.82);
    --border:         rgba(56, 120, 255, 0.18);
    --border-bright:  rgba(56, 120, 255, 0.45);
    --accent-blue:    #3878ff;
    --accent-cyan:    #00d4ff;
    --accent-violet:  #7c5cfc;
    --text-primary:   #e8edf8;
    --text-secondary: #8a9bbf;
    --text-muted:     #4f6080;
    --glow-blue:      0 0 24px rgba(56, 120, 255, 0.30);
    --glow-cyan:      0 0 18px rgba(0, 212, 255, 0.22);
    --radius-sm:      8px;
    --radius-md:      14px;
    --radius-lg:      20px;
    --font-display:   'Syne', sans-serif;
    --font-body:      'DM Sans', sans-serif;
    --transition:     all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* ---------- BACKGROUND ---------- */
.stApp {{
    background-image: url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    font-family: var(--font-body);
}}

.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    backdrop-filter: blur(12px) saturate(0.6);
    -webkit-backdrop-filter: blur(12px) saturate(0.6);
    background:
        radial-gradient(ellipse 80% 60% at 20% 0%,  rgba(56,120,255,0.12) 0%, transparent 70%),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(124,92,252,0.10) 0%, transparent 70%),
        rgba(5, 10, 20, 0.82);
    z-index: -1;
}}

/* ---------- GLOBAL TEXT ---------- */
html, body, [class*="css"], .stApp {{
    font-family: var(--font-body) !important;
    color: var(--text-primary);
}}

/* ---------- MAIN CONTENT AREA ---------- */
.main .block-container {{
    background: transparent;
    padding: 2rem 2.5rem;
    max-width: 1200px;
}}

/* ---------- HEADER ---------- */
h1 {{
    font-family: var(--font-display) !important;
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    background: linear-gradient(120deg, #ffffff 0%, var(--accent-cyan) 55%, var(--accent-violet) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.15rem !important;
    line-height: 1.15 !important;
}}

h2, [data-testid="stHeading"] h2, .stApp h2 {{
    font-family: var(--font-display) !important;
    font-size: 3.2rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em !important;
}}

h3, h4 {{
    font-family: var(--font-display) !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em;
}}

/* ---------- CAPTION / SUBTITLE ---------- */
.stApp [data-testid="stCaptionContainer"] p,
.stApp .stCaption {{
    color: #c8d8f0 !important;
    font-size: 1.25rem !important;
    font-weight: 300 !important;
    letter-spacing: 0.01em;
}}

/* ---------- BODY TEXT ---------- */
p, span, li, div {{
    color: var(--text-primary);
    font-size: 0.95rem;
    line-height: 1.7;
}}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, rgba(5,10,20,0.96) 0%, rgba(11,21,38,0.98) 100%) !important;
    border-right: 1px solid var(--border) !important;
    backdrop-filter: blur(20px);
}}

[data-testid="stSidebar"] * {{
    color: var(--text-primary) !important;
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    font-family: var(--font-display) !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.01em;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] span {{
    color: var(--text-secondary) !important;
    font-size: 0.88rem !important;
}}

[data-testid="stSidebar"] strong {{
    color: var(--accent-cyan) !important;
    font-weight: 600 !important;
}}

[data-testid="stSidebar"] hr {{
    border-color: var(--border) !important;
    margin: 1rem 0 !important;
}}

/* ---------- SIDEBAR LOGO / TITLE AREA ---------- */
[data-testid="stSidebar"] .stMarkdown:first-child h1 {{
    background: linear-gradient(120deg, #ffffff, var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1.4rem !important;
}}

/* ---------- FILE UPLOADER ---------- */
[data-testid="stFileUploader"] {{
    background: rgba(56, 120, 255, 0.06) !important;
    border: 1px dashed var(--border-bright) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.5rem !important;
    transition: var(--transition) !important;
}}

[data-testid="stFileUploader"]:hover {{
    border-color: var(--accent-cyan) !important;
    background: rgba(0, 212, 255, 0.05) !important;
    box-shadow: var(--glow-cyan);
}}

[data-testid="stFileUploader"] * {{
    color: var(--text-secondary) !important;
}}

[data-testid="stFileUploader"] button {{
    background: rgba(56,120,255,0.15) !important;
    border: 1px solid var(--border-bright) !important;
    color: var(--accent-cyan) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    transition: var(--transition) !important;
}}

[data-testid="stFileUploader"] button:hover {{
    background: rgba(56,120,255,0.28) !important;
    box-shadow: var(--glow-blue) !important;
}}

/* ---------- BUTTONS ---------- */
.stButton > button {{
    font-family: var(--font-display) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em;
    border-radius: var(--radius-sm) !important;
    background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-violet) 100%) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 0.55rem 1.4rem !important;
    transition: var(--transition) !important;
    box-shadow: 0 2px 12px rgba(56,120,255,0.25) !important;
    position: relative;
    overflow: hidden;
}}

.stButton > button::after {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.08), transparent);
    pointer-events: none;
}}

.stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(56,120,255,0.45) !important;
    background: linear-gradient(135deg, #4d8fff 0%, #9575ff 100%) !important;
}}

.stButton > button:active {{
    transform: translateY(0px) !important;
}}

/* ---------- CHAT INPUT ---------- */
[data-testid="stChatInput"] {{
    background: rgba(13, 22, 44, 0.90) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--radius-md) !important;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 0 0 transparent;
    transition: var(--transition);
}}

[data-testid="stChatInput"]:focus-within {{
    border-color: var(--accent-cyan) !important;
    box-shadow: var(--glow-cyan) !important;
}}

[data-testid="stChatInput"] textarea {{
    background: transparent !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
    caret-color: var(--accent-cyan) !important;
}}

[data-testid="stChatInput"] textarea::placeholder {{
    color: var(--text-muted) !important;
}}

[data-testid="stChatInput"] button {{
    background: var(--accent-blue) !important;
    border-radius: 8px !important;
    transition: var(--transition) !important;
}}

[data-testid="stChatInput"] button:hover {{
    background: var(--accent-cyan) !important;
}}

/* ---------- CHAT MESSAGES ---------- */
.stChatMessage {{
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.75rem !important;
    backdrop-filter: blur(10px);
    transition: var(--transition);
}}

.stChatMessage:hover {{
    border-color: var(--border-bright) !important;
}}

/* User message accent */
.stChatMessage[data-testid*="user"] {{
    border-left: 3px solid var(--accent-blue) !important;
    background: rgba(56, 120, 255, 0.07) !important;
}}

/* Assistant message accent */
.stChatMessage[data-testid*="assistant"] {{
    border-left: 3px solid var(--accent-cyan) !important;
    background: rgba(0, 212, 255, 0.04) !important;
}}

.stChatMessage p {{
    color: var(--text-primary) !important;
    font-size: 0.95rem !important;
    line-height: 1.75 !important;
}}

/* ---------- SOURCE BOX ---------- */
.source-box {{
    background: rgba(56, 120, 255, 0.06);
    border-left: 3px solid var(--accent-blue);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 0.65rem 0.9rem;
    margin-bottom: 0.5rem;
    font-size: 0.82rem !important;
    color: var(--text-secondary) !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    letter-spacing: 0.01em;
    word-break: break-all;
    transition: var(--transition);
}}

.source-box:hover {{
    background: rgba(56, 120, 255, 0.12);
    border-left-color: var(--accent-cyan);
    color: var(--text-primary) !important;
}}

/* ---------- EXPANDERS ---------- */
[data-testid="stExpander"] {{
    background: rgba(13, 22, 44, 0.65) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    backdrop-filter: blur(8px);
    transition: var(--transition);
    margin-top: 0.5rem !important;
}}

[data-testid="stExpander"]:hover {{
    border-color: var(--border-bright) !important;
}}

[data-testid="stExpander"] summary {{
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em;
    padding: 0.6rem 0.9rem !important;
}}

[data-testid="stExpander"] summary:hover {{
    color: var(--accent-cyan) !important;
}}

/* ---------- STATUS BOX ---------- */
[data-testid="stStatus"] {{
    background: var(--bg-card) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--radius-md) !important;
    backdrop-filter: blur(10px);
    padding: 1rem !important;
}}

[data-testid="stStatus"] * {{
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
}}

/* ---------- INFO / ALERT BOX ---------- */
.stAlert {{
    background: rgba(56, 120, 255, 0.08) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--radius-md) !important;
    backdrop-filter: blur(8px);
}}

.stAlert p {{
    color: var(--text-primary) !important;
    font-size: 0.9rem !important;
}}

/* ---------- DIVIDER ---------- */
hr {{
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}}

/* ---------- COLUMNS / FEATURE TILES ---------- */
[data-testid="stHorizontalBlock"] > div {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.4rem 1.2rem;
    backdrop-filter: blur(10px);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}}

[data-testid="stHorizontalBlock"] > div::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan));
    opacity: 0;
    transition: var(--transition);
}}

[data-testid="stHorizontalBlock"] > div:hover {{
    border-color: var(--border-bright);
    box-shadow: var(--glow-blue);
    transform: translateY(-2px);
}}

[data-testid="stHorizontalBlock"] > div:hover::before {{
    opacity: 1;
}}

/* ---------- SPINNER ---------- */
[data-testid="stSpinner"] * {{
    color: var(--accent-cyan) !important;
    border-top-color: var(--accent-cyan) !important;
}}

/* ---------- SCROLLBAR ---------- */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}

::-webkit-scrollbar-track {{
    background: rgba(5, 10, 20, 0.5);
}}

::-webkit-scrollbar-thumb {{
    background: rgba(56, 120, 255, 0.35);
    border-radius: 99px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: rgba(56, 120, 255, 0.6);
}}

/* ---------- SELECTION ---------- */
::selection {{
    background: rgba(56, 120, 255, 0.3);
    color: #ffffff;
}}

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
st.markdown("""
<style>
.big-title { font-size: 2.9rem !important; font-weight: 800 !important; letter-spacing: -0.03em !important; background: linear-gradient(120deg, #ffffff 0%, #00d4ff 55%, #7c5cfc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0 !important; line-height: 1.9 !important; }
</style>
<p class='big-title'>AI Document Assistant</p>
""", unsafe_allow_html=True)

st.markdown("<p style='font-size:1.25rem; color:#c8d8f0; font-weight:300; margin-top:-1rem; letter-spacing:0.01em;'>Upload documents and instantly extract insights using AI.</p>", unsafe_allow_html=True)

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