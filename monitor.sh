#!/bin/bash

# Output file
LOG_FILE="resource_usage.csv"
echo "Timestamp,Container,CPU,MemUsage,MemPerc" > $LOG_FILE

echo "Starting Monitoring..."

# Function to collect stats
collect_stats() {
    while true; do
        TIMESTAMP=$(date +%s)
        # Capture stats for our specific containers
        # Format: Name, CPU Percentage, Memory Usage, Memory Percentage
        # We strip the '%' sign for easier CSV parsing if needed, but keeping it for readability now
        podman stats --no-stream --format "{{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}" go-bench java-bench python-bench | while read line; do
            echo "$TIMESTAMP,$line" >> $LOG_FILE
        done
        sleep 1
    done
}

# Start collection in background
collect_stats &
PID=$!

echo "Running Load Test..."
k6 run loadtest.js

echo "Load Test Complete."
kill $PID
echo "Monitoring stopped."
echo ""
echo "=== Resource Usage Summary ==="
python3 analyze_stats.py
