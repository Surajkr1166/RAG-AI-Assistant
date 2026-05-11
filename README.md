

```markdown
# 🔍 RAG-AI-Assistant — Adaptive RAG Chatbot

An intelligent, agentic AI chatbot that dynamically routes queries using **LangGraph**, retrieves context from uploaded documents, searches the web in real-time, or answers from general knowledge — all powered by **Groq LLaMA 3.1** (free & fast).

---

## 🚀 Features

- 📄 **Document Upload** — Upload PDF or TXT files for context-aware Q&A
- 🧠 **Adaptive Query Routing** — Automatically routes to Vector Search, Web Search, or General LLM
- ✅ **Corrective RAG (CRAG)** — Grades retrieved docs, rewrites queries if needed
- 🔍 **Real-time Web Search** — Uses Tavily API when indexed docs aren't enough
- 💬 **Chat History** — Persistent conversation history via MongoDB Atlas
- ⚡ **Fast Inference** — Powered by Groq LLaMA 3.1 (free tier)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq LLaMA 3.1 (Free) |
| Orchestration | LangGraph + LangChain |
| Vector DB | FAISS |
| Web Search | Tavily API |
| Embeddings | HuggingFace sentence-transformers |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | MongoDB Atlas |

---

## 📁 Project Structure

```
IntelliSearch/
├── intellisearch/
│   ├── api/          # FastAPI routes
│   ├── config/       # Prompts & settings
│   ├── core/         # App config & logger
│   ├── db/           # MongoDB client
│   ├── llms/         # Groq LLM setup
│   ├── memory/       # Chat history
│   ├── models/       # Pydantic models
│   ├── rag/          # Graph builder, retriever, agent
│   └── tools/        # Routing & grading tools
├── streamlit_app/    # Frontend UI
├── main.py           # FastAPI entry point
├── requirements.txt
└── .env.example
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/Surajkr1166/RAG-AI-Assistant.git
cd RAG-AI-Assistant
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
HF_TOKEN=your_huggingface_token
MONGODB_URL=your_mongodb_atlas_url
MONGODB_DB_NAME=intellisearch
```

### 5. Run FastAPI backend
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Run Streamlit frontend
```bash
streamlit run streamlit_app/home.py
```

---

## 🧠 How It Works

```
User Query
    ↓
[Query Classifier]
    ↓           ↓           ↓
 index        general      search
    ↓           ↓           ↓
Vector DB    General    Web Search
  + CRAG       LLM       (Tavily)
    ↓           ↓           ↓
         [Final Answer]
```

---

## 🔑 Get Free API Keys

- **Groq** → https://console.groq.com
- **Tavily** → https://app.tavily.com
- **HuggingFace** → https://huggingface.co/settings/tokens
- **MongoDB Atlas** → https://www.mongodb.com/atlas

---

## 👨‍💻 Author

**Suraj Kumar**  
