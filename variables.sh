export PROJECT_ID="co-oortiz-internal";
export BUCKET_NAME="co-oortiz-internal";
export GOOGLE_APPLICATION_CREDENTIALS="${PWD}/keras_webapi/service-key.json";
export GOOGLE_CLOUD_PROJECT="co-oortiz-internal";

export MODEL_NAME="keras_model";
export MODEL_VERSION="6";
export JOB_NAME="${MODEL_NAME}_${MODEL_VERSION}";
export JOB_DIR="gs://${BUCKET_NAME}";
export MODEL_BINARIES="${JOB_DIR}/${MODEL_NAME}/${MODEL_VERSION}/";

export PORT="8080";
export REGION="us-east1";
export MODEL_PORT="9090";

export BODY_PATH="${PWD}/keras_training/model_doc/prediction_input.json";
export BODY=`[[ -e "${BODY_PATH}" ]] && echo "$(cat ${BODY_PATH})" || echo 'NONE'`;
