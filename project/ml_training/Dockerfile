FROM tensorflow/tensorflow:nightly

ARG KEY_SERVICE="./service-key.json"
ARG MODEL_VERSION="9"
ARG JOB_DIR="co-oortiz-internal-model"
ARG GIT_REPO="https://poxstone@github.com/poxstone/ai-platform-keras.git"
ARG GIT_HASH=""
ARG GIT_BRANCH=""
ARG GIT_TAG="trained"

ENV APP_PATH="/app"
ENV MODEL_VERSION="${MODEL_VERSION}"
ENV JOB_DIR="${JOB_DIR}"
ENV GOOGLE_APPLICATION_CREDENTIALS="${APP_PATH}/service-key.json"
ENV GIT_REPO="${GIT_REPO}"
ENV GIT_HASH="${GIT_HASH}"
ENV GIT_BRANCH="${GIT_BRANCH}"
ENV GIT_TAG="${GIT_TAG}"

WORKDIR ${APP_PATH}

RUN pip install google-cloud-storage cloudml-hypertune pandas
RUN apt install -y git

COPY ./ ${APP_PATH}
COPY ${KEY_SERVICE} ${APP_PATH}/

ENTRYPOINT python -m trainer.task  --job-version ${MODEL_VERSION} --trainded-dir ${JOB_DIR}
