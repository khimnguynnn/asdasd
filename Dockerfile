FROM python:3.9-slim

WORKDIR /app

COPY main.py /app/main.py

RUN pip install smtplib kubernetes

ENV SMTP_HOST=""
ENV SMTP_PORT=""
ENV SMTP_USERNAME=""
ENV SMTP_PASSWORD=""
ENV FROM_EMAIL=""
ENV TO_EMAILS=""

CMD ["python", "/app/main.py"]
