FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libglib2.0-dev && \
    pip install flask

COPY . /app

CMD ["python", "main.py"]