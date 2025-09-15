# Resource Optimizer Agent — MVP (Updated)

**Purpose:** Small Python tool that analyzes cloud billing/usage JSON and surfaces the top cost drivers (by service, resource or nested tag).

## What’s included
- `src/optimizer.py` — core logic with dot-notation nested key support (e.g., tags.env)
- `sample_data/sample_billing.json` — sample input data
- `tests/test_optimizer.py` — pytest tests
- `requirements.txt` — minimal dependencies (pytest)
- `Dockerfile` — containerize the optimizer for local runs
- `docker-compose.yml` — convenience compose file for local development
- `issues/TODOs.md` — project tasks and roadmap

## Quick start (local)
```bash
# create venv (recommended)
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
pip install -r requirements.txt

# run tests
pytest -q

# run against sample data
python -m src.optimizer sample_data/sample_billing.json --key tags.env --top 5 --output report.json
```
