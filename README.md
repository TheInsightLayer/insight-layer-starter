# 🧠 Insight Layer Starter

📝 MIT Licensed | Built with Python, Streamlit, LangChain, FAISS

This repository demonstrates a minimal working example of an Insight Layer using documentation as the base use case. It captures key insights from files, stores them with metadata, and provides a simple UI for browsing and reusing those insights.

> The Insight Layer is a new approach to capturing and reusing what your organization already knows. By extracting key insights from documentation and surfacing them in context, this project helps reduce rework and improve cross-team awareness.

![Insight Layer Preview](preview.png)

---

## ✅ What’s Included

- GPT-powered extraction pipeline
- Streamlit UI with tagging, re-extract, and CSV export
- FastAPI backend for programmatic access
- FAISS embedding store for semantic search
- Audit logging and lightweight JSON/SQLite storage

---

## 🧠 Use Case

Start with plain text (`.txt`) documentation and automatically extract reusable insights from it.

Example use cases:
- Internal process docs
- Meeting notes
- Onboarding guides
- Strategy decks (exported to `.txt`)

---

## ✨ Features

- Ingest plain text documentation
- Extract insights using OpenAI or fallback mock logic
- Store insights with tags, related topics, and source metadata
- Streamlit UI to view, search, and re-extract insights
- Semantic search using FAISS (optional)
- Audit log of created and re-extracted insights
- CSV export
- REST API with FastAPI
- Dockerfile for API deployment

---

## 🔧 Tech Stack

- Python
- LangChain + OpenAI (GPT-4 or GPT-3.5)
- Streamlit
- SQLite + JSON
- FAISS (for semantic search)
- FastAPI

---

## ⚡ Quickstart

### 1. Setup

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
cp .env.example .env        # Add your OpenAI API key
```

### 2. Ingest and Extract

```bash
python src/ingest/ingest_docs.py docs/example-guide.txt
python src/extract/extract_insights.py
```

### 3. Optional: Enable Semantic Search

```bash
python scripts/embed_existing_insights.py
```

This will embed all current insights to power semantic search in the UI.

---

## 🎛️ Streamlit UI

```bash
streamlit run src/ui/streamlit_app.py
```

Search by:
- **Keyword**: literal match in insight text, tags, or related topics
- **Semantic**: FAISS-powered similarity search

Also supports:
- Re-extraction via GPT
- Manual insight entry
- CSV export
- Audit logging

---

## 🔌 API Access (Optional)

Run:
```bash
uvicorn app.api:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

You can:
- Get insights
- Submit new ones
- Extract via LLM

See [app/README.md](app/README.md) for more details.

---

## 🖥️ Quick Launch

### ▶️ Windows

```bash
run_ui.bat
```

### 🐧 macOS/Linux

```bash
chmod +x run_ui.sh
./run_ui.sh
```

---

## 📁 Directory Structure

```
insight-layer-starter/
├── .env.example
├── README.md
├── preview.png
├── requirements.txt
├── Dockerfile
├── LICENSE
├── CONTRIBUTING.md
├── run_ui.bat
├── run_ui.sh
├── docs/
│   └── example-guide.txt
├── data/
│   ├── raw_text.txt
│   ├── insights.json
│   ├── insights.db
│   ├── audit_log.jsonl
│   └── insight_faiss/
├── src/
│   ├── ingest/
│   ├── extract/
│   ├── ui/
│   ├── storage/
│   └── utils/
├── app/
│   └── api.py
├── scripts/
│   └── embed_existing_insights.py
```

---

## 💡 Insight Format

```json
{
  "source": "example-guide.txt",
  "insight": "Clear roles reduce confusion in cross-functional projects.",
  "tags": ["roles", "collaboration"],
  "timestamp": "2025-04-20T14:00:00",
  "related_to": ["project kickoff", "team setup"]
}
```

---

## 🤝 Contributing

PRs welcome! To contribute:

1. Fork the repo
2. Create a new branch
3. Open a pull request with your improvements

---

## 🔗 Resources

- [OpenAI API](https://platform.openai.com/)
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [FastAPI](https://fastapi.tiangolo.com/)

---

