FROM python:3.11-slim

WORKDIR /app

# system deps (if needed for chromadb)
RUN apt-get update && apt-get install -y build-essential libpq-dev git libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
