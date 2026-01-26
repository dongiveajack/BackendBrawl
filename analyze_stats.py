import csv
import sys
import re

def parse_size(size_str):
    """Parse memory size string to MB."""
    if not size_str:
        return 0.0
    units = {"B": 1e-6, "kB": 1e-3, "MB": 1, "GB": 1e3, "TB": 1e6}
    # Matches number and unit (e.g. 12.5MB)
    match = re.match(r"([0-9.]+)([a-zA-Z]+)", size_str)
    if not match:
        return 0.0
    val, unit = match.groups()
    return float(val) * units.get(unit, 1)

def parse_cpu(cpu_str):
    """Parse CPU percentage string."""
    return float(cpu_str.replace('%', ''))

stats = {}

try:
    with open('resource_usage.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            container = row['Container']
            if container not in stats:
                stats[container] = {'cpu': [], 'mem': []}
            
            try:
                cpu = parse_cpu(row['CPU'])
                mem_str = row['MemUsage'].split('/')[0].strip() # Handle '12MB / 1GB' format if raw podman output
                # My monitor.sh output format was {{.MemUsage}} which creates "12.5MB" directly usually, 
                # but depending on podman version it might range.
                # Let's assume the CSV contains just the usage part or clean if needed. 
                # The `monitor.sh` used {{.MemUsage}}, which outputs user-friendly string e.g. "12.34MB"
                
                mem = parse_size(mem_str)
                
                stats[container]['cpu'].append(cpu)
                stats[container]['mem'].append(mem)
            except ValueError:
                continue
except FileNotFoundError:
    print("No data found.")
    sys.exit(1)

print(f"{'Service':<15} | {'Avg CPU (%)':<12} | {'Max CPU (%)':<12} | {'Avg Mem (MB)':<12} | {'Max Mem (MB)':<12}")
print("-" * 75)

for container, data in stats.items():
    if not data['cpu']:
        continue
        
    avg_cpu = sum(data['cpu']) / len(data['cpu'])
    max_cpu = max(data['cpu'])
    avg_mem = sum(data['mem']) / len(data['mem'])
    max_mem = max(data['mem'])
    
    print(f"{container:<15} | {avg_cpu:<12.2f} | {max_cpu:<12.2f} | {avg_mem:<12.2f} | {max_mem:<12.2f}")
