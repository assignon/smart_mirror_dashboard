FROM python:3.9-rc-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ['uwsgi', "app.ini"]