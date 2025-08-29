FROM python:3.12.8-slim

# ====== base setup ======
ENV YOUR_ENV=production \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.8.2

WORKDIR /backend

# ====== system dependencies ======
RUN apt-get update && \
    apt-get install -y sudo gcc g++ python3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ====== install poetry ======
RUN pip install "poetry==$POETRY_VERSION"

# ====== copy and install Python dependencies ======
COPY backend/poetry.lock backend/pyproject.toml /backend/
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi

# ====== backend application files ======
RUN mkdir -p /mnt/credentials
ADD backend/app /backend/app
ADD backend/alembic /backend/alembic
ADD backend/common /backend/common
ADD backend/scripts /backend/scripts
ADD backend/etl /backend/etl
COPY backend/alembic.ini /backend/alembic.ini
COPY backend/start.sh /backend/start.sh

# ====== environment adjustments ======
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.12/site-packages"

# remove unused dist-packages to prevent false positives for trivy
RUN rm -rf /usr/local/lib/python3.12/dist-packages

# add testing tools
RUN pip install pytest==7.3.1 coverage==7.2.7

# non-root user setup
RUN ln -f -s /usr/bin/python3.12 /usr/bin/python3 && \
    groupadd -r nonroot && \
    useradd -r -g nonroot nonroot && \
    chown -R nonroot:nonroot /backend && \
    chmod 755 /backend/start.sh

USER nonroot
EXPOSE 8000
CMD ["./start.sh"]
