FROM harbor.cicd.s15m.nl/ictu-devops-pub/algreg_etl_base AS buildstep

# Make sure these are set, either here or in the base image.
ENV YOUR_ENV=${YOUR_ENV}
# ENV YOUR_ENV=${YOUR_ENV} \
#   PYTHONFAULTHANDLER=1 \
#   PYTHONUNBUFFERED=1 \
#   PYTHONHASHSEED=random \
#   PIP_NO_CACHE_DIR=off \
#   PIP_DISABLE_PIP_VERSION_CHECK=on \
#   PIP_DEFAULT_TIMEOUT=100 \
#   POETRY_VERSION=1.2.2
  
WORKDIR /etl

ADD /etl/app /etl/app
ADD /etl/common /etl/common
COPY /etl/poetry.lock /etl/poetry.lock
COPY /etl/pyproject.toml /etl/pyproject.toml
COPY /etl/start.sh /etl/start.sh


RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-interaction --no-ansi

FROM harbor.cicd.s15m.nl/ictu-devops-pub/python:3.11.1-lunar-devops_base_0.2
WORKDIR /etl
COPY --from=buildstep /etl /etl

# Copy python binaries ensuring a clean install without overhead
COPY --from=buildstep /usr/local/lib /usr/local/lib
RUN ln -f -s /usr/bin/python3.11 /usr/bin/python3
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.11/site-packages"

# remove unused dist-packages to prevent false positives for trivy
RUN rm -rf /usr/local/lib/python3.11/dist-packages

# add testing tools
# RUN pip install pytest==7.3.1 coverage==7.2.7

# # add non root user for security with home directory for test files
RUN groupadd -r nonroot &&\
  useradd -r -g nonroot nonroot
RUN chown -R nonroot:nonroot /etl

# make start.sh executable
RUN chmod 777 /etl/start.sh

USER nonroot
EXPOSE 8000:8000
CMD ["./start.sh"]
