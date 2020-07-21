# AI Platform project (keras sample)

- **keras_training:** Train model local, docker container and AI Platform (Jobs and Model)
- **keras_serving:** Serve model on Docker container
- **keras_webapi:** Expose Endpoints to consumer AI Platform model and Docker serving model 

> **Original:** [keras census](https://github.com/GoogleCloudPlatform/cloudml-samples/tree/master/census/keras)


## 1. Install enviroment python

- Create new service account download json key and save it into keras_webapi and keras_training
- Execute following commands
```bash
python3 -m virtualenv ./venv;
source ./venv/bin/activate;
# install for weapp
pip install -r ./keras_webapi/requirements.txt;
# install for model
pip install -r ./keras_training/requirements.txt;
```


## 2. Load enviroment variables

Edit and load variables for all commands run.
```bash
source ./variables.sh;
```
Create service account
```bash
# create service account
gcloud iam service-accounts create "${SERVICE_ACCOUNT_NAME}" --display-name "${SERVICE_ACCOUNT_NAME}";
# add permissions
gcloud projects add-iam-policy-binding "${GOOGLE_CLOUD_PROJECT}" --member "serviceAccount:${SERVICE_ACCOUNT_EMAIL}" --role roles/editor;
# create key
gcloud iam service-accounts keys create "${SERVICE_KEY_FILE}" --iam-account "${SERVICE_ACCOUNT_EMAIL}";

# move to folders
cp "${SERVICE_KEY_FILE}" "keras_training/";
cp "${SERVICE_KEY_FILE}" "keras_webapi/";
```

## 3. Build and run containers

### 3.A Docker training
```bash
# build
docker build -t "gcr.io/${GOOGLE_CLOUD_PROJECT}/${MODEL_NAME}:${MODEL_VERSION}" \
  --build-arg "MODEL_VERSION=${MODEL_VERSION}" \
  --build-arg "JOB_DIR=${JOB_DIR}" -f "./keras_training/Dockerfile" "./keras_training";
# run
docker run -it --rm "gcr.io/${GOOGLE_CLOUD_PROJECT}/${MODEL_NAME}:${MODEL_VERSION}";
```

### 3.B Keras GCloud training

- Train in Google AI Platform
```bash
cd "./keras_training";
gcloud ai-platform jobs submit training "${JOB_NAME}" --project "${GOOGLE_CLOUD_PROJECT}" \
  --stream-logs \
  --python-version 3.7 \
  --runtime-version 2.1 \
  --job-dir "${JOB_DIR}" \
  --package-path trainer \
  --module-name trainer.task \
  --region "${REGION}" \
  -- \
  --job-version "${MODEL_VERSION}" --trainded-dir "${BUCKET_NAME}" \
  --verbosity DEBUG;
```


## 4. Server in Google and local

### 4.A Server docker local
```bash
# download model from GS
mkdir -p "./${MODEL_NAME}";
gsutil cp -r "gs://${BUCKET_NAME}/${MODEL_NAME}/${MODEL_VERSION}" "./${MODEL_NAME}/";
# build
docker build -t "gcr.io/${GOOGLE_CLOUD_PROJECT}/keras_serve:${MODEL_VERSION}" \
  --build-arg "MODEL_NAME=${MODEL_NAME}" \
  --build-arg "MODEL_LOCATION=./${MODEL_NAME}/${MODEL_VERSION}/" \
  -f "./keras_serve/Dockerfile" "./";
# run
docker run -it --rm --name keras_serve --net host -e APP_PORT=9090 -p 9090:9090 -p 8500:8500 "gcr.io/${GOOGLE_CLOUD_PROJECT}/keras_serve:${MODEL_VERSION}";

# curl prediction
curl -i -X POST -H "Content-Type: application/json" "http://localhost:9090/v1/models/${MODEL_NAME}:predict" -d "${BODY}";
```

### 4.B Serve Google AI Platform
```bash
# create model
gcloud ai-platform models create "${MODEL_NAME}" --regions "${REGION}" --project "${GOOGLE_CLOUD_PROJECT}";
# create version
gcloud ai-platform versions create "${JOB_NAME}" --project "${GOOGLE_CLOUD_PROJECT}" \
  --model "${MODEL_NAME}" \
  --framework "tensorflow" \
  --origin "${MODEL_BINARIES}" \
  --runtime-version "2.1" \
  --python-version "3.7";

# enter to UI page to tests
echo "https://console.cloud.google.com/ai-platform/models/${MODEL_NAME}/versions/${JOB_NAME}/test-and-use?project=${GOOGLE_CLOUD_PROJECT}";
```


### 5 Keras webapi

```bash
# build
docker build -t "gcr.io/${GOOGLE_CLOUD_PROJECT}/keras_webapi:${MODEL_VERSION}" -f "./keras_webapi/Dockerfile" "./keras_webapi";
# run app
docker run -it --rm --name keras_webapi -p 8080:8080 -e "GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" \
  "gcr.io/${GOOGLE_CLOUD_PROJECT}/keras_webapi:${MODEL_VERSION}";
```

## 6. Test curls
```bash
# to AI Platform
curl -X POST -H 'Content-Type: application/json' "http://localhost:${PORT}/api/keras/${JOB_NAME}" -d "${BODY}";
# to Docker
curl -X POST -H 'Content-Type: application/json' "http://localhost:${PORT}/api/keras-host" -d "${BODY}";
```

## Predictions Review

| **platform**    | 9                 | 7                  | 8                   | 5                  | 10                  | 2                  | 4                  | 6                  | 6                  | 1                |
|----------------:|-------------------|:------------------:|--------------------:|-------------------:|--------------------:|-------------------:|-------------------:|-------------------:|-------------------:|-----------------:|
| **Local**       | 1.1202626e-07     | 3.1044985e-07      | 1.1162208e-07       | 1.0275202e-06      | 4.7845255e-08       | 4.6996918e-04      | 1.3370330e-06      | 1.3858461e-02      | 4.8601555e-07      | 9.8566818e-01    |
| **Container**   | -10.4870024       | -9.46771336        | -10.4906168         | -8.27083111        | -11.3377647         | -2.14531326        | -8.00752735        | 1.23867071         | -9.01949501        | 5.5030942        |
| **GCP**         | -10.4870023727417 | -9.467713356018066 | -10.490616798400879 | -8.270831108093262 | -11.337764739990234 | -2.145313262939453 | -8.007527351379395 | 1.2386707067489624 | -9.019495010375977 | 5.50309419631958 |
```json




# from ide
[,,,,,,      ,      ,      ,      ]
# from container
[,,,,,,        ,        ,         ,        ]
# from AI Platform
[,,,,, , , , ,  ]
```