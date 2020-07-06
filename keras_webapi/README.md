# app get model

```bash
pip install -r requirements.txt;
```

## variables
```bash
source "../variables.sh";
```

## Get prediction
```bash
BODY="$(cat ./keras_model/model_doc/prediction_input.json)";
curl -X POST -H 'Content-Type: application/json' "http://localhost:8080/api/keras/${JOB_NAME}" -d "${BODY}";
```
