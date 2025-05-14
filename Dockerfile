FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
# ✅ Increase pip timeout to 100 seconds, set retries to 10
RUN pip install --default-timeout=100 --retries=10 --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY .env .env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
