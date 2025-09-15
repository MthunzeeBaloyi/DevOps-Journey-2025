#!/usr/bin/env python3
"""Resource Optimizer Agent - summarizer with optional S3 fetch.

Usage:
    # local file:
    python -m src.optimizer sample_data/sample_billing.json --key tags.env --top 5

    # from S3:
    python -m src.optimizer dummy.json --s3-bucket my-bucket --s3-key path/to/billing.json --key tags.env --top 5
"""
import json
import argparse
import os
import tempfile
from collections import defaultdict
from typing import Any, Dict, List, Optional

# boto3 is optional at runtime; import when used
try:
    import boto3
    from botocore.exceptions import ClientError
except Exception:
    boto3 = None
    ClientError = Exception  # fallback


def get_field_value(record: Dict[str, Any], key: str) -> Optional[Any]:
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
    """Summarize total cost by `key` (e.g., 'service' or 'resource_id')."""
    totals = defaultdict(float)
    for r in records:
        k = get_field_value(r, key) or r.get(key) or r.get('service') or 'unknown'
        try:
            cost = float(r.get('cost', 0) or 0)
        except Exception:
            cost = 0.0
        totals[k] += cost
    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    return sorted_totals[:top_n]


def load_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path: str, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def fetch_s3_to_file(bucket: str, key: str) -> str:
    """Download an S3 object to a temporary file and return local path."""
    if boto3 is None:
        raise RuntimeError("boto3 is not installed. add boto3 to requirements.txt")
    s3 = boto3.client('s3')
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        with open(tmp.name, 'wb') as f:
            s3.download_fileobj(bucket, key, f)
        return tmp.name
    except ClientError as e:
        # cleanup on error
        try:
            os.unlink(tmp.name)
        except Exception:
            pass
        raise


def main():
    parser = argparse.ArgumentParser(description='Resource Optimizer Agent - summarize costs')
    parser.add_argument('input_file', nargs='?', help='Path to billing JSON file (array of records)', default=None)
    parser.add_argument('--key', help='Field to aggregate by (supports dot-notation, default: service)', default='service')
    parser.add_argument('--top', type=int, help='Top N results', default=5)
    parser.add_argument('--output', help='Optional output JSON file', default=None)
    parser.add_argument('--s3-bucket', help='S3 bucket to download input file from', default=None)
    parser.add_argument('--s3-key', help='S3 object key to download', default=None)
    args = parser.parse_args()

    temp_input = None
    try:
        # decide input path: prefer S3 if both flags provided
        if args.s3_bucket and args.s3_key:
            temp_input = fetch_s3_to_file(args.s3_bucket, args.s3_key)
            input_path = temp_input
        elif args.input_file:
            input_path = args.input_file
        else:
            raise SystemExit("Error: no input file specified. Provide a local file or --s3-bucket/--s3-key")

        records = load_json(input_path)
        top = summarize_costs(records, key=args.key, top_n=args.top)
        output = [{'key': k, 'cost': c} for k, c in top]
        if args.output:
            write_json(args.output, output)
        else:
            print(json.dumps(output, indent=2))

    finally:
        if temp_input and os.path.exists(temp_input):
            try:
                os.unlink(temp_input)
            except Exception:
                pass


if __name__ == '__main__':
    main()

