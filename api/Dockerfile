FROM python:3.8.16

WORKDIR /api
RUN python3 -m venv /opt/venv

### Install base dependencies
RUN /opt/venv/bin/pip install \
    psycopg2-binary \
    pysftp \
    redis \
    requests \
    pyyaml \
    uwsgi==2.0.19.1 \
    airflow-client-python==2.5.1

### Install dependencies
COPY sa.json sa.json
COPY api api
RUN cd api && /opt/venv/bin/pip install -r requirements.txt

## Environment variable
ENV MODE=dev
ENV GOOGLE_APPLICATION_CREDENTIALS=/api/sa.json

### Run application
EXPOSE 5000
CMD ["/opt/venv/bin/uwsgi", "--ini", "/api/src/service.ini"]