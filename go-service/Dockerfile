# Build Stage
FROM golang:1.23-alpine AS builder

WORKDIR /app
COPY . .
RUN go mod tidy
RUN go mod download

RUN CGO_ENABLED=0 GOOS=linux go build -o /app/service main.go
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/service main.go

# Runtime Stage
FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/service .

EXPOSE 8080
CMD ["./service"]
