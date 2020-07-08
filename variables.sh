export PROJECT_ID="co-oortiz-internal";
export BUCKER_NAME="co-oortiz-internal";
export GOOGLE_APPLICATION_CREDENTIALS="${PWD}/keras_webapi/service-key.json";
export GOOGLE_CLOUD_PROJECT="co-oortiz-internal";
export JOB_DIR="gs://${BUCKER_NAME}";
export JOB_NAME="keras_test_002";
export MODEL_NAME="keras_model";
export MODEL_BINARIES="${JOB_DIR}/${MODEL_NAME}/${JOB_NAME}/";
export MODEL_VERSION="${JOB_NAME}";
export PORT="8080";
export REGION="us-east1";

export BODY_PATH="./keras_training/model_doc/prediction_input.json";
export BODY=`[[ -e "${BODY_PATH}" ]] && echo "$(cat ${BODY_PATH})" || echo 'NONE'`;