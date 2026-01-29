# 🥊 BackendBrawl: Go vs Java vs Python

**The ultimate high-concurrency showdown.**

This project benchmarks three functionally identical microservices—**Go (Standard Lib)**, **Java (Spring Boot)**, and **Python (FastAPI)**—to see which runtime reigns supreme under load.

We push them to the limit with **2500 concurrent users (VUs)** hammering a Redis cache, measuring:
- ⚡️ **Latency**: Who responds fastest?
- 🚀 **Throughput**: Who handles the most RPS?
- 💻 **Efficiency**: Who burns the least CPU/RAM?

## 🏗 Project Structure

- **`go-service/`**: Go implementation using `net/http` and `go-redis`.
- **`java-service/`**: Java implementation using Spring Boot 3 and Lettuce.
- **`java-native-service/`**: GraalVM Native Image version of the Java service.
- **`python-service/`**: Python implementation using FastAPI and `redis-py` (async).
- **`prometheus.yml`**: Configuration for Prometheus scraping all services.
- **`loadtest.js`**: K6 load testing script with scenarios for each language.
- **`monitor.sh`**: Shell script to orchestrate the test and capture real-time CPU/Memory stats.
- **`analyze_stats.py`**: Python script to generate a resource usage summary after the test.
- **Observability**: Prometheus (metrics storage) and Grafana (visualization).

## 🚀 Prerequisites

- **Podman** (or Docker)
- **k6** (for load testing)
- **Python 3** (for analysis script)

## 🛠 Setup

### 1. Create a Network
Create a dedicated network to minimize latency between services and Redis.
```bash
podman network create bench-net
```

### 2. Start Redis
```bash
podman run -d --name redis --network bench-net -p 6379:6379 redis:latest
# Populate test data
podman exec redis redis-cli set test_key "Hello World"
```

### 3. Build Service Images
```bash
podman build -t go-bench ./go-service
podman build -t java-bench ./java-service
podman build -t python-bench ./python-service
```

### 4. Run Services
Start all services on the shared network.
```bash
# Go (Port 8080)
podman run -d --name go-bench --network bench-net -p 8080:8080 --env REDIS_HOST=redis go-bench

# Java (Port 8081)
podman run -d --name java-bench --network bench-net -p 8081:8081 --env SPRING_DATA_REDIS_HOST=redis java-bench

# Python (Port 8082)
podman run -d --name python-bench --network bench-net -p 8082:8082 --env REDIS_HOST=redis python-bench
```

### 5. Setup Observability
```bash
# Start Prometheus
podman run -d --name prometheus --network bench-net -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml:Z prom/prometheus

# Start Grafana
podman run -d --name grafana --network bench-net -p 3000:3000 grafana/grafana
```
- **Prometheus**: Access at [http://localhost:9090](http://localhost:9090)
- **Grafana**: Access at [http://localhost:3000](http://localhost:3000) (Default: `admin/admin`)

## 📊 Running the Benchmark

We use a consolidated script to fail-safe the process: run the load test, capture streaming metrics, and generate a final report.

```bash
chmod +x monitor.sh
./monitor.sh
```

**What happens:**
1.  **Metric Collection**: `podman stats` runs in the background, logging CPU/Mem to `resource_usage.csv` and printing to console.
2.  **Load Test**: `k6 run loadtest.js` executes. By default, it runs scenarios sequentially (Go → Java → Python) to isolate results.
3.  **Analysis**: `analyze_stats.py` parses the CSV and prints a summary table of Average/Max CPU and Memory usage per service.

## 📈 Optimization Details

The services are tuned for high concurrency (tested with up to 2000 concurrent VUs):
- **Connection Pooling**: All services are configured with a pool size of **2500 connections** to prevent queuing bottlenecks.
- **Network**: Uses a private bridge network (`bench-net`) to bypass host-level proxy overhead on macOS.
- **Logging**: Application-level logging is disabled/minimized to focus on raw throughput.

## 📝 Configuration

- **`loadtest.js`**: Adjust VUs, duration, and stages in the `options.scenarios` object.
- **Ports**:
    - Go: `:8080/metrics`
    - Java: `:8081/actuator/prometheus`
    - Python: `:8082/metrics`
    - Java Native: `:8083/actuator/prometheus`

## 🧹 Cleanup

Stop and remove all project containers and network:

```bash
# Stop containers
podman rm -f redis go-bench java-bench python-bench

# Remove network
podman network rm bench-net
```

## ☸️ Kubernetes Deployment

To deploy the entire stack to Kubernetes (e.g., Minikube, Kind):

### 1. Apply Manifests
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/prometheus.yaml
kubectl apply -f k8s/grafana.yaml
kubectl apply -f k8s/services.yaml
```

### 2. Access Dashboards
```bash
# Prometheus
kubectl port-forward svc/prometheus -n backend-brawl 9090:9090

# Grafana
kubectl port-forward svc/grafana -n backend-brawl 3000:3000
```

## ❓ Troubleshooting

- **`Connection refused`**: Ensure all containers are running on the `bench-net` network.
- **High Latency (>10ms)**: Check if you are running with sufficient connection pool size (2500+) and using the Podman network instead of localhost binding.
- **`monitor.sh: permission denied`**: Run `chmod +x monitor.sh`.

## 🎯 Expected Results

With the current optimization (2500 connections + internal networking), you should observe:
- **RPS**: ~3000-6000+ (depending on hardware)
- **Latency (p99)**: Single-digit milliseconds (e.g., 2-8ms)
- **No queuing errors** or timeouts.
