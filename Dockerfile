FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn langchain-openai openai python-dotenv

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]