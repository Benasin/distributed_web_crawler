# Dockerfile for Application Server

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

COPY ./start.sh .
RUN ["chmod", "+x", "start.sh"]
COPY ./src .

CMD [ "./start.sh" ]