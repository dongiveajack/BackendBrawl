# Python Service (FastAPI)

## Prerequisites
- Python 3.8+
- Redis running on `localhost:6379`

## Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
# --log-level error to disable unnecessary logging
uvicorn main:app --port 8082 --log-level error
```

The service listens on port 8082 (to avoid conflict with others).
Endpoint: `GET /cache`
