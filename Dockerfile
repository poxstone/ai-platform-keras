ARG PYTHON_VERSION=3.7-alpine

FROM python:${PYTHON_VERSION}

ENV APP_PORT=8080
ENV APP_PATH='/app'

#RUN pip3 install

COPY ./app_src/ $APP_PATH

ENTRYPOINT ['python']
