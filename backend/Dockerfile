# FIX IMAGE URI TO THE RELEVANT OPENSOURCE URI
FROM <..>./algreg_base AS buildstep

# Make sure these are set, either here or in the base image.
ENV YOUR_ENV=${YOUR_ENV} 
# ENV PYTHONFAULTHANDLER=1 \
#   PYTHONUNBUFFERED=1 \
#   PYTHONHASHSEED=random \
#   PIP_NO_CACHE_DIR=off \
#   PIP_DISABLE_PIP_VERSION_CHECK=on \
#   PIP_DEFAULT_TIMEOUT=100 \
#   POETRY_VERSION=1.2.2

RUN mkdir -p /mnt/credentials
WORKDIR /backend

ADD /backend/app /backend/app
ADD /backend/alembic /backend/alembic
ADD /backend/common /backend/common
ADD /backend/scripts /backend/scripts
ADD /backend/etl /backend/etl
COPY /backend/alembic.ini /backend/alembic.ini
COPY /backend/poetry.lock /backend/poetry.lock
COPY /backend/pyproject.toml /backend/pyproject.toml
COPY /backend/start.sh /backend/start.sh

RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-interaction --no-ansi

FROM <..>./python:3.11.1-lunar-devops_base_0.2

WORKDIR /backend

COPY --from=buildstep /backend /backend

# Copy python binaries ensuring a clean install without overhead
COPY --from=buildstep /usr/local/lib /usr/local/lib
RUN ln -f -s /usr/bin/python3.11 /usr/bin/python3
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.11/site-packages"

# remove unused dist-packages to prevent false positives for trivy
RUN rm -rf /usr/local/lib/python3.11/dist-packages

# add testing tools
RUN pip install pytest==7.3.1 coverage==7.2.7

# # add non root user for security with home directory for test files
RUN groupadd -r nonroot &&\
  useradd -r -g nonroot nonroot
RUN chown -R nonroot:nonroot /backend

# make start.sh executable
RUN chmod 777 /backend/start.sh

USER nonroot
EXPOSE 8000:8000
CMD ["./start.sh"]
