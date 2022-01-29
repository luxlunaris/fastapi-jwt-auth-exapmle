FROM python:3.9 AS base
COPY . /auth
WORKDIR /auth
RUN pip install -r requirements.txt
EXPOSE 8001
EXPOSE 5678