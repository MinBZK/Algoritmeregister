FROM python:3.11.3-slim

ENV YOUR_ENV=production \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2

WORKDIR /etl

COPY ./requirements.txt /backend/requirements.txt

RUN apt-get update
RUN apt-get -y install sudo
RUN sudo apt-get -y install gcc g++ python3-dev 
RUN pip install -r /backend/requirements.txt 
RUN pip install "poetry==$POETRY_VERSION"

# Cleans up cache -> Reduces size for download.
RUN sudo apt-get clean


