# 🧠 Insight Layer API

A FastAPI-powered service to serve, create, and extract insights using the Insight Layer backend.

---

## 🔧 Prerequisites

Install Python packages:

```bash
pip install fastapi uvicorn langchain-openai python-dotenv openai
```

(Optional: also install SQLite tools, FAISS, or other optional integrations.)

---

## 🚀 Running Locally

```bash
uvicorn app.api:app --reload
```

Then open:
- Interactive docs: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

---

## 🔌 Endpoints

### `GET /insights`
Query insights by keyword or tag.

Example:
```
/insights?keyword=roles
```

---

### `POST /insights`
Submit a structured insight manually.

```json
{
  "insight": "Checklists reduce variability in medical procedures.",
  "tags": ["checklist", "process"],
  "related_to": ["surgery", "safety"],
  "source": "manual.txt"
}
```

---

### `POST /extract`
Extract a structured insight from raw text.

```json
{
  "text": "Our team often fails to align unless we assign clear roles early."
}
```

---

## 🐳 Docker Deployment

### 1. Dockerfile

```dockerfile
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn langchain-openai openai python-dotenv

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Build & Run

```bash
docker build -t insight-layer-api .
docker run -p 8000:8000 insight-layer-api
```

Then open `http://localhost:8000/docs`.

---

## 📁 Files

- `app/api.py` → FastAPI app
- `Dockerfile` → Containerization setup
- `README.md` → API usage guide