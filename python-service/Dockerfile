FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8082

# Using standard uvicorn worker with 4 workers for concurrency
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082", "--workers", "4", "--log-level", "error"]
