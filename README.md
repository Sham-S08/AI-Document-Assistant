<div align="center">

# 🚀 AI Document Assistant

**Chat with your PDFs like never before**  
*Upload • Ingest • Ask • Get smart answers*

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white&style=flat-square)
![Groq](https://img.shields.io/badge/Groq-00A0E9?logo=groq&logoColor=white&style=flat-square)
![Chroma](https://img.shields.io/badge/Chroma-DB-4C1?logo=chroma&logoColor=white&style=flat-square)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

<br>

**An AI-powered RAG system** that lets you upload PDFs and interact with them through a beautiful chat interface — powered by **LangChain**, **Streamlit**, **ChromaDB**, and lightning-fast **Groq** inference.

</div>

---

# ✨ Features

- 📤 **Drag & drop PDF upload**
- ⚡ **One-click ingestion** (chunking + embeddings)
- 🧠 **Smart RAG pipeline** with source citations
- 💬 **Real-time chat interface**
- 🔒 **Persistent Chroma vector store**
- ⚡ **Blazing-fast responses** via Groq (Llama-3 / Mixtral etc.)
- 🧩 **Modular & extensible architecture**

---

# 🚀 Quick Start (2 minutes)

## 1️⃣ Clone & Install

```bash
git clone https://github.com/Sham-S08/AI-Document-Assistant.git
cd AI-Document-Assistant
pip install -r requirements.txt
```

---

## 2️⃣ Add your Groq Key

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

Get a free API key from:

```text
https://console.groq.com
```

---

## 3️⃣ Launch the Application

```bash
streamlit run app/main.py
```

Then open:

```text
http://localhost:8501
```

Done! 🎉

---

# 📁 Project Structure

```text
AI-Document-Assistant/
│
├── app/                 # Main application
│   ├── main.py          # Streamlit UI + chat
│   ├── rag_pipeline.py  # RAG chain
│   ├── ingest.py        # Document processor
│   ├── retriever.py
│   ├── embeddings.py
│   └── prompts.py
│
├── vectorstore/         # Chroma DB (auto-created)
├── data/documents/      # Drop your PDFs here
├── loaders/             # Custom PDF loaders
├── text_splitters/      # Chunking strategies
├── ui/                  # UI components
├── utils/               # Config & helpers
│
├── requirements.txt
└── .env                 # Your API key
```

---

# 📸 Demo (Coming Soon)

Run the project locally and you'll see:

```text
• Clean Streamlit sidebar
• File uploader
• Ingest button
• Chat interface
• Source citations with answers
```

---

# 🤝 Contributing

Love the project? Pull requests are welcome!

### 1️⃣ Fork the repository

### 2️⃣ Create a feature branch

```bash
git checkout -b feature/amazing-feature
```

### 3️⃣ Commit your changes

```bash
git commit -m "Add amazing feature"
```

### 4️⃣ Push to GitHub

```bash
git push origin feature/amazing-feature
```

### 5️⃣ Open a Pull Request 🚀

---

<div align="center">

### ❤️ Built with Groq + LangChain + Streamlit

**Made by Sham-S08 • MIT License**

</div>
