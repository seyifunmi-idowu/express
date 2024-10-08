# Multi stage build

# Builder stage
FROM python:3.8-bullseye as builder

# "allow-releaseinfo-change" update local with new release
# install "wget" and "gnupg" and answer "-y" yes to the command line question
RUN apt-get --allow-releaseinfo-change update \
    && apt-get install wget gnupg git -y

# get postgres repo and save
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc
RUN apt-key add ACCC4CF8.asc

RUN apt-get update \
    && apt-get install -y git

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app

ENV CELERY_WORKER_RUNNING=true


# App stage
FROM python:3.8.0-slim-buster as app

# Copy only necessary files from the builder stage
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

WORKDIR /app

# Install only necessary runtime dependencies
RUN apt-get update \
    && apt-get install -y libpq5 postgresql-client \
    && apt-get clean

ENV PATH="/opt/venv/bin:$PATH"
ENV CELERY_WORKER_RUNNING=true

COPY ./docker.sh /docker.sh
RUN chmod +x /docker.sh

CMD ["/docker.sh"]
