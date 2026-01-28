# Go Service

## Prerequisites
- Go 1.23+
- Redis running on `localhost:6379`

## Run
```bash
# Install dependencies
go mod tidy

# Run application
go run main.go
```

The service listens on port 8080.
Endpoints:
- `GET /cache`: Get value from Redis
- `GET /metrics`: Prometheus metrics
