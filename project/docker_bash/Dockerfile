FROM debian:9

USER root

ENV SCRIPT_PATH="/etc/r_scripts"

RUN apt-get update -y
RUN apt-get install -y r-base mysql-client

COPY ./ ${SCRIPT_PATH}/

WORKDIR $SCRIPT_PATH

ENTRYPOINT /bin/sh ${SCRIPT_PATH}/entrypoint.sh
