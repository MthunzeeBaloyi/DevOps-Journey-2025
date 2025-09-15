FROM python:3.10-slim

WORKDIR /app

COPY src/ ./src
COPY requirements.txt .

RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python", "-m", "src.optimizer"]
