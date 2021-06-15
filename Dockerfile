FROM python:3.9.1
# FROM ubuntu:16.04

MAINTAINER "yanick007.dev@gmail.com"

# run apt-get update -y && \
#     apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip

RUN pip install typing

RUN pip install -r requirements.txt

RUN chmod +x ./entrypoint.sh

EXPOSE 5000

# COPY . /app

# ENTRYPOINT [ "gunicorn", "--config", "gunicorn_config.py", "app.wsgi:app" ]
ENTRYPOINT [ "sh", "entrypoint.sh" ]
# CMD [ "python", "app.py" ]