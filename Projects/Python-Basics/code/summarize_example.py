# summarize_example.py
# Tiny example showing a cost summarizer pattern similar to Resource Optimizer Agent

from collections import defaultdict
import json

def summarize_costs(records, key='service', top_n=5):
    totals = defaultdict(float)
    for r in records:
        k = r.get(key) or r.get('service', 'unknown')
        try:
            cost = float(r.get('cost', 0) or 0)
        except Exception:
            cost = 0.0
        totals[k] += cost
    items = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    return items[:top_n]

if __name__ == '__main__':
    sample = [
        {"service":"EC2", "cost": 12.5},
        {"service":"S3", "cost": 3.25},
        {"service":"EC2", "cost": 4.75},
    ]
    print(summarize_costs(sample, key='service'))
