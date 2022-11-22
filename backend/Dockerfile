# FROM harbor.cicd.s15m.nl/ictu-devops-pub/rid_base:3.11_alpine_3.16
FROM harbor.cicd.s15m.nl/ictu-devops-pub/rid_base:3.11-slim2-0.1

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2

RUN apt-get update && \
  apt-get -y install sudo

ADD ./backend/app /backend/app
ADD ./backend/alembic /backend/alembic
ADD ./backend/common /backend/common
COPY ./backend/alembic.ini /backend/alembic.ini
COPY ./backend/poetry.lock /backend/poetry.lock
COPY ./backend/pyproject.toml /backend/pyproject.toml
COPY ./backend/start.sh /backend/start.sh

WORKDIR /backend

RUN sudo apt-get -y install gcc g++ && \
  pip install "poetry==$POETRY_VERSION" && \
  poetry config virtualenvs.create false && \
  poetry install --without dev --no-interaction --no-ansi && \
  apt-get remove --purge -y gcc g++ && \
  pip uninstall -y "poetry==$POETRY_VERSION" && \
  sudo apt-get clean

# Expose ports
EXPOSE 8000:8000

ENV PYTHONPATH="$PYTHONPATH:/:/backend"

# Run the application
RUN sudo chmod 777 /backend/start.sh

CMD ["./start.sh"]