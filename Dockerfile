FROM python:3.11-slim

WORKDIR /app

COPY requirements-service.txt .

RUN pip install --no-cache-dir -r requirements-service.txt

COPY models/ ./models/

ENV LLAMA_MODEL_PATH=/app/models/qwen-q4km.gguf

COPY app/ ./app/

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]