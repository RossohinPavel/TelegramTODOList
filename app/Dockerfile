FROM python:3.12.4-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get install -y ffmpeg libavcodec-extra

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
