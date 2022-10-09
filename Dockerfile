FROM python:3.10-slim-buster AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    python3-dev \
    build-essential

WORKDIR /app

COPY requirements.txt /app/requirements.txt 
RUN pip install -r /app/requirements.txt

FROM python:3.10-slim-buster

COPY --from=base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    python3-dev \
    build-essential

WORKDIR /app
COPY . /app

EXPOSE 5000

