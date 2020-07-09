FROM ubuntu:18.04

ARG MODEL_NAME="keras_model"
ARG MODEL_LOCATION="./keras_training/keras_model/1/"

ENV APP_PATH="/model"
ENV MODEL_NAME="${MODEL_NAME}"
ENV APP_PORT=9090

WORKDIR $APP_PATH

RUN apt update -y && apt upgrade -y && apt install -y curl gnupg2 python3  python3-dev
RUN echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" \
    | tee /etc/apt/sources.list.d/tensorflow-serving.list && curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | \
    apt-key add -; apt-get update -y
RUN apt install -y tensorflow-model-server && apt upgrade -y tensorflow-model-server

COPY ${MODEL_LOCATION} ${APP_PATH}/1

# use pd to consume, download from cloud Storage
ENTRYPOINT tensorflow_model_server --model_base_path=${APP_PATH}/ --port=8500 --rest_api_port=$APP_PORT --model_name=${MODEL_NAME}
