FROM python:3.11-slim
RUN apt-get update && apt-get install -y snmp && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip install --no-cache-dir kafka-python
COPY . .
