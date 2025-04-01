# Dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN pip install kubernetes

COPY monitor_events.py .

CMD ["python", "monitor_events.py"]
