# Go Service

## Prerequisites
- Go 1.21+
- Redis running on `localhost:6379`

## Run
```bash
# Install dependencies
go mod tidy

# Run application
go run main.go
```

The service listens on port 8080.
Endpoint: `GET /cache`
