#!/usr/bin/env python3
"""Resource Optimizer Agent - simple summarizer of costs by service/resource.

Usage:
    python -m src.optimizer sample_data/sample_billing.json --top 5 --output report.json
"""
import json
import argparse
from collections import defaultdict
from typing import Any, Dict, List


def get_field_value(record: Dict[str, Any], key: str):
    """Support nested keys with dot notation, e.g. 'tags.env'."""
    if not key:
        return None
    parts = key.split(".")
    current = record
    for p in parts:
        if isinstance(current, dict) and p in current:
            current = current[p]
        else:
            return None
    return current


def summarize_costs(records: List[Dict[str, Any]], key='service', top_n=5):
    """Summarize total cost by `key` (e.g., 'service' or 'resource_id').

    records: list of dicts containing at least the `key` and `cost` fields.
    Returns a list of (key_value, total_cost) sorted descending by cost.
    """
    totals = defaultdict(float)
    for r in records:
        # support nested key like 'tags.env'
        k = get_field_value(r, key) or r.get(key) or r.get('service') or 'unknown'
        try:
            cost = float(r.get('cost', 0) or 0)
        except Exception:
            cost = 0.0
        totals[k] += cost
    # sort descending
    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    return sorted_totals[:top_n]


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Resource Optimizer Agent - summarize costs')
    parser.add_argument('input_file', help='Path to billing JSON file (array of records)')
    parser.add_argument('--key', help='Field to aggregate by (supports dot-notation, default: service)', default='service')
    parser.add_argument('--top', type=int, help='Top N results', default=5)
    parser.add_argument('--output', help='Optional output JSON file', default=None)
    args = parser.parse_args()

    records = load_json(args.input_file)
    top = summarize_costs(records, key=args.key, top_n=args.top)
    output = [{'key': k, 'cost': c} for k, c in top]
    if args.output:
        write_json(args.output, output)
    else:
        print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
