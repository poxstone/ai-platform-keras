FROM gcr.io/deeplearning-platform-release/tf2-gpu.2-2
#FROM tensorflow/tensorflow:nightly

ARG KEY_SERVICE="./service-key.json"
ARG MODEL_NAME="keras"
ARG MODEL_VERSION="9"
ARG JOB_DIR="co-oortiz-internal-model"
ARG GIT_REPO="https://poxstone:3c321d61b02ecd820620011df94af74a00aafbd2@github.com/poxstone/ai-platform-keras.git"
ARG GIT_COMMIT="5f6ee1f22b37e7f128c8ebeb8a735aea57636c70"
ARG GIT_TAGNAME="trained"
ARG ACCOUNTSERVICE_EMAIL="ai-platform@co-oortiz-internal.iam.gserviceaccount.com"
ARG GOOGLE_CLOUD_PROJECT="co-oortiz-internal"

ENV APP_PATH="/app"
ENV MODEL_NAME="${MODEL_NAME}"
ENV MODEL_VERSION="${MODEL_VERSION}"
ENV JOB_DIR="${JOB_DIR}"
ENV GOOGLE_APPLICATION_CREDENTIALS="${APP_PATH}/service-key.json"
ENV ACCOUNTSERVICE_EMAIL="${ACCOUNTSERVICE_EMAIL}"
ARG GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT}"
ENV GIT_REPO="${GIT_REPO}"
ENV GIT_COMMIT="${GIT_COMMIT}"
ENV GIT_TAGNAME="${GIT_TAGNAME}"

WORKDIR ${APP_PATH}

RUN apt-get update -y; \
    apt-get install -y wget;
RUN pip install google-cloud-storage cloudml-hypertune pandas

# install git
RUN apt install -y git && \
    git config --global user.name "docker@devops.com" && \
    git config --global user.email "docker@devops.com"

RUN wget -nv \
    https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
    mkdir /root/tools && \
    tar xvzf google-cloud-sdk.tar.gz -C /root/tools && \
    rm google-cloud-sdk.tar.gz && \
    /root/tools/google-cloud-sdk/install.sh --usage-reporting=false \
        --path-update=false --bash-completion=false \
        --disable-installation-options && \
    rm -rf /root/.config/* && \
    ln -s /root/.config /config && \
    # Remove the backup directory that gcloud creates
    rm -rf /root/tools/google-cloud-sdk/.install/.backup; \
    # create links
    ln -s /root/tools/google-cloud-sdk/bin/gsutil /bin/gsutil; \
    ln -s /root/tools/google-cloud-sdk/bin/gcloud /bin/gcloud;

COPY ./ ${APP_PATH}
COPY ${KEY_SERVICE} ${APP_PATH}/

# GCP authorize
RUN gcloud auth activate-service-account "${ACCOUNTSERVICE_EMAIL}" --key-file "${GOOGLE_APPLICATION_CREDENTIALS}" -q;

ENTRYPOINT /bin/sh ./entrypoint.sh
