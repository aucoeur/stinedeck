FROM python:3.9.1-slim-buster

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY ./src /app

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run"]
