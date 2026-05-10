# 🤖 RAG Chatbot

A Retrieval-Augmented Generation (RAG) based AI chatbot built using FastAPI and Streamlit.  
The application enables intelligent question-answering over custom documents using LLM-powered semantic search and retrieval pipelines.

---

## 🚀 Features

- Retrieval-Augmented Generation (RAG) pipeline
- AI-powered document question answering
- FastAPI backend APIs
- Streamlit interactive frontend
- Semantic search using embeddings
- Vector database integration
- Context-aware response generation
- Modular and scalable architecture

---

## 🛠️ Tech Stack

- Python
- FastAPI
- Streamlit
- LangChain
- OpenAI API
- Vector Database (FAISS/ChromaDB)
- Embedding Models

---


## ⚡ Installation

Clone the repository:

```bash
git clone https://github.com/Raju995/RAG-Chatbot.git
cd RAG-Chatbot
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## ▶️ Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend server:

```plaintext
http://127.0.0.1:8000
```

---

## ▶️ Run Frontend

```bash
streamlit run frontend/app.py
```

Frontend will run at:

```plaintext
http://localhost:8501
```

---

## 🧠 How It Works

1. User uploads or queries documents
2. Text is converted into embeddings
3. Relevant chunks are retrieved using semantic search
4. Retrieved context is passed to the LLM
5. AI generates context-aware responses

---

## 🔮 Future Improvements

- Multi-document support
- Chat history memory
- Authentication system
- PDF and DOCX ingestion
- Hybrid search
- Multi-agent RAG workflows
- Cloud deployment

---

## 📸 Screenshots

_Add screenshots here_

---

## 👨‍💻 Author

Raju Chatterjee

- GitHub: https://github.com/Raju995

---
