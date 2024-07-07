FROM python:3.10.13-slim

WORKDIR /app

COPY . /app/

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

RUN pip install -r requirements.txt

CMD uvicorn --app-dir ./app  main:app --port=8000 --host=0.0.0.0