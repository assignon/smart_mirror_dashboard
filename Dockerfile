FROM node:lts-alpine

WORKDIR /app

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend .

Run npm run build



FROM python:3.9.1
# FROM ubuntu:16.04

MAINTAINER "yanick007.dev@gmail.com"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

# ADD . /app

RUN pip install --upgrade pip

RUN pip install typing

RUN pip install gunicorn

RUN pip install --no-cache-dir -r requirements.txt


# EXPOSE 8000

COPY . /app

# ENTRYPOINT [ "gunicorn", "--config", "gunicorn_config.py", "wsgi" ]