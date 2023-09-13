FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*
    
ENV WORKERS 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ .

CMD gunicorn --bind 0.0.0.0:5000 --workers $WORKERS --worker-class=gevent app:app