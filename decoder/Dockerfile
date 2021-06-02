FROM python:3.7-slim

RUN mkdir /app
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

VOLUME ["/app/encoded"]

CMD flask run --host=0.0.0.0 --port=6666