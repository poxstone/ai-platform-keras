FROM tensorflow/tensorflow:nightly

ARG KEY_SERVICE="./service-key.json"
ARG MODEL_VERSION="9"
ARG JOB_DIR="co-oortiz-internal-model"
ARG GIT_REPO="https://poxstone@github.com/poxstone/ai-platform-keras.git"
ARG GIT_COMMIT="5f6ee1f22b37e7f128c8ebeb8a735aea57636c70"
ARG GIT_TAGNAME="trained"

ENV APP_PATH="/app"
ENV MODEL_VERSION="${MODEL_VERSION}"
ENV JOB_DIR="${JOB_DIR}"
ENV GOOGLE_APPLICATION_CREDENTIALS="${APP_PATH}/service-key.json"
ENV GIT_REPO="${GIT_REPO}"
ENV GIT_COMMIT="${GIT_COMMIT}"
ENV GIT_TAGNAME="${GIT_TAGNAME}"

WORKDIR ${APP_PATH}

RUN pip install google-cloud-storage cloudml-hypertune pandas
RUN apt install -y git && \
    git config --global user.name "docker@devops.com" && \
    git config --global user.email "docker@devops.com"

COPY ./ ${APP_PATH}
COPY ${KEY_SERVICE} ${APP_PATH}/

ENTRYPOINT /bin/sh ./entrypoint.sh
