FROM python:alpine

RUN apk add make && pip install pdm

ENTRYPOINT [ "sleep", "inf" ]
WORKDIR /var/app
ENV PYTHONPATH=/var/app