FROM python:3.11.3-slim

# ====== base setup ======
ENV YOUR_ENV=production \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2

WORKDIR /etl

# install system deps needed for building Python packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    libffi-dev \
    libssl-dev \
    curl \
    ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# copy and install requirements
COPY etl/base_image/requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip \
 && pip install -r /backend/requirements.txt \
 && pip install "poetry==$POETRY_VERSION"

# ====== etl setup ======
ADD etl/app /etl/app
ADD etl/common /etl/common
COPY etl/poetry.lock /etl/poetry.lock
COPY etl/pyproject.toml /etl/pyproject.toml
COPY etl/start.sh /etl/start.sh

# clear poetry cache and install dependencies
RUN poetry cache clear pypi --all \
 && poetry config virtualenvs.create false \
 && poetry install --without dev --no-interaction --no-ansi

# remove unused dist-packages to reduce image size and trivy noise
RUN rm -rf /usr/local/lib/python3.11/dist-packages

# add non-root user
RUN groupadd -r nonroot && useradd -r -g nonroot nonroot \
 && chown -R nonroot:nonroot /etl

# make start.sh executable
RUN chmod 755 /etl/start.sh

USER nonroot
EXPOSE 8000
CMD ["./start.sh"]
