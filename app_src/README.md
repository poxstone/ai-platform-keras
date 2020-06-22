# app get model

```bash
pip install -r requirements.txt;
```


## variables
```bash
PROJECT="co-oortiz-internal";
BUCKER_NAME="co-oortiz-internal";
REGION="us-east1";
MODEL_NAME="keras_model";
MODEL_VERSION="${JOB_NAME}";
JOB_NAME="keras_test_002";
JOB_DIR="gs://${BUCKER_NAME}";
MODEL_BINARIES="${JOB_DIR}/${MODEL_NAME}/${JOB_NAME}/";
```

## Get prediction
```bash
BODY="$(cat ../model_doc/prediction_input.json)";
curl -X POST -H 'Content-Type: application/json' "http://localhost:8080/api/keras/${JOB_NAME}" -d "${BODY}";
```
