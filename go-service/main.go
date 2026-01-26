package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/redis/go-redis/v9"
)

var (
	rdb *redis.Client
	ctx = context.Background()
)

type Response struct {
	Value string `json:"value"`
}

func init() {
	// Use connection pooling for Redis
	redisHost := os.Getenv("REDIS_HOST")
	if redisHost == "" {
		redisHost = "localhost"
	}

	rdb = redis.NewClient(&redis.Options{
		Addr:         redisHost + ":6379",
		MinIdleConns: 500,
		PoolSize:     2500, // Matched to 2000+ VUs
	})
}

func handleCache(w http.ResponseWriter, r *http.Request) {
	// Single responsibility: HTTP -> Redis GET -> Response
	val, err := rdb.Get(ctx, "test_key").Result()
	if err != nil && err != redis.Nil {
		// Minimal error handling, just return 500 if Redis fails
		// If key doesn't exist (redis.Nil), we return empty string or "null" depending on preference,
		// but prompt says "Read... Return JSON value". I'll return empty string for missing key to keep specific structure.
		// However, for benchmarking, we usually assume the key exists.
		http.Error(w, "Redis Error", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	// Minimal JSON serialization
	json.NewEncoder(w).Encode(Response{Value: val})
}

func main() {
	// Disable unnecessary logging (default go log is quiet unless called)

	http.HandleFunc("/cache", handleCache)

	// Use a custom server for better control if needed, but http.ListenAndServe is fine for this scope
	// Go's net/http is high performance enough.
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
