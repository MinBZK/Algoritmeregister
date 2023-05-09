# FROM harbor.cicd.s15m.nl/ictu-devops-pub/rid_base:3.11_alpine_3.16
FROM harbor.cicd.s15m.nl/ictu-devops-pub/rid_base:3.11-slim2-0.1 as buildstep

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

# #TODO
# RUN apt-get -y purge libpython3.9* python3.9*
# RUN apt-get install --upgrade libtasn1-6 linux-libc-dev
# #TODO

ADD /backend/app /backend/app
ADD /backend/alembic /backend/alembic
ADD /backend/common /backend/common
COPY /backend/alembic.ini /backend/alembic.ini
COPY /backend/poetry.lock /backend/poetry.lock
COPY /backend/pyproject.toml /backend/pyproject.toml
COPY /backend/start.sh /backend/start.sh

WORKDIR /backend

# RUN sudo apt-get -y install gcc g++ && \
#   pip install "poetry==$POETRY_VERSION" && \
#   poetry config virtualenvs.create false && \
#   poetry install --without dev --no-interaction --no-ansi && \
#   apt-get remove --purge -y gcc g++ && \
#   pip uninstall -y "poetry==$POETRY_VERSION" && \
#   sudo apt-get clean

RUN sudo apt-get -y install gcc g++
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-interaction --no-ansi
RUN apt-get remove --purge -y gcc g++
RUN pip uninstall -y "poetry==$POETRY_VERSION"
RUN sudo apt-get clean

FROM harbor.cicd.s15m.nl/ictu-devops-pub/python:3.11.1-lunar-devops_base_0.2
WORKDIR /backend

COPY --from=buildstep /backend /backend
COPY --from=buildstep /usr/local/lib /usr/local/lib
RUN ln -f -s /usr/bin/python3.11 /usr/bin/python3
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.11/site-packages"

RUN sudo chmod 777 /backend/start.sh

EXPOSE 8000:8000
CMD ["./start.sh"]
