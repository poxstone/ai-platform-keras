FROM python:3.7-alpine

ENV APP_PORT=8080
ENV APP_PATH="/app"
ENV GUNICORN_MODULE="main"
ENV GUNICORN_CALLABLE="app"
ENV APP_PATH="gs://co-grupoexito-motrecaban-dev-models"
ENV WORKERS="22838"
ENV TIMEOUT=240
ENV GOOGLE_APPLICATION_CREDENTIALS="${APP_PATH}/service-key.json"
#ENV GOOGLE_CLOUD_PROJECT="";

# builds
RUN apk add build-base libffi-dev openssl-dev python3-dev linux-headers 

# app
RUN apk add --no-cache python3 \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip gunicorn \
    && adduser -D -h $APP_PATH $GUNICORN_USER

COPY ./ $APP_PATH
RUN pip3 install -r $APP_PATH/requirements.txt
RUN chown -R ${GUNICORN_USER}:${GUNICORN_USER} $APP_PATH

EXPOSE $APP_PORT

USER $GUNICORN_USER
WORKDIR $APP_PATH
ENTRYPOINT $APP_PATH/entrypoint.sh
