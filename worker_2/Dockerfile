# Dockerfile for Celery Worker Server

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .
COPY ./start.sh .
RUN ["chmod", "+x", "start.sh"]

CMD ["./start.sh"]