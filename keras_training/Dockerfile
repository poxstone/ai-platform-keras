FROM tensorflow/tensorflow:nightly

ARG KEY_SERVICE="./service-key.json"
ARG MODEL_VERSION="3"
ARG JOB_DIR="co-oortiz-internal"

ENV APP_PATH="/app"
ENV MODEL_VERSION="${MODEL_VERSION}"
ENV JOB_DIR="${JOB_DIR}"
ENV GOOGLE_APPLICATION_CREDENTIALS="${APP_PATH}/service-key.json"

WORKDIR ${APP_PATH}

RUN pip install google-cloud-storage cloudml-hypertune pandas

COPY ./ ${APP_PATH}
COPY ${KEY_SERVICE} ${APP_PATH}/

ENTRYPOINT python -m trainer.task  --job-version ${MODEL_VERSION} --trainded-dir ${JOB_DIR}
