# Resource Optimizer Agent — MVP

**Solomon Baloyi — DevOps / Cloud Portfolio Project**

A small CLI tool that reads cloud billing-like JSON and summarizes cost by a key (supports nested keys like `tags.env`). Built as a portfolio piece to demonstrate Python, testing, Docker, and CI.

---

## Features
- Aggregate costs by any field (supports dot-notation, e.g. `tags.env`)
- Optional download from S3 (`--s3-bucket` + `--s3-key`)
- Simple CLI and JSON output
- Unit tests with `pytest`
- Dockerfile for local container runs
- CI workflow (GitHub Actions) runs tests automatically

---

## Quickstart

### Prerequisites
- Python 3.10+
- Docker (optional)
- Git

### Setup (local)
```bash
cd Projects/Resource-Optimizer-Agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
### Demo UI (Streamlit)
A demo Streamlit app is available at `Projects/Resource-Optimizer-Agent/ui/streamlit_app.py`.

Run locally:
```bash
cd Projects/Resource-Optimizer-Agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt streamlit pandas boto3
streamlit run ui/streamlit_app.py
