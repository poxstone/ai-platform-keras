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
pip install -r ./keras_training/requiremetns.txt;
```


## 2. Load enviroment Variables

Edit and load variables for all commands run.
```bash
source ./variables.sh;
```


## 3. Build and run containers

### 3.A Docker training
```bash
# build
docker build -t "gcr.io/${PROJECT_ID}/${MODEL_NAME}:${MODEL_VERSION}" \
  --build-arg "MODEL_VERSION=${MODEL_VERSION}" \
  --build-arg "JOB_DIR=${JOB_DIR}" -f "./keras_training/Dockerfile" "./keras_training";
# run
docker run -it --rm "gcr.io/${PROJECT_ID}/${MODEL_NAME}:${MODEL_VERSION}";
```

### 3.B Keras GCloud training

- Train in Google AI Platform
```bash
cd "./keras_training";
gcloud ai-platform jobs submit training "${JOB_NAME}" --project "${PROJECT_ID}" \
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
gsutil cp -r "gs://${BUCKER_NAME}/${MODEL_NAME}/${MODEL_VERSION}" "./${MODEL_NAME}/";
# build
docker build -t "gcr.io/${PROJECT_ID}/keras_serve:${MODEL_VERSION}" \
  --build-arg "MODEL_NAME=${MODEL_NAME}" \
  --build-arg "MODEL_LOCATION=./${MODEL_NAME}/${MODEL_VERSION}/" \
  -f "./keras_serve/Dockerfile" "./";
# run
docker run -it --rm --name keras_serve --net host -e APP_PORT=9090 -p 9090:9090 -p 8500:8500 "gcr.io/${PROJECT_ID}/keras_serve:${MODEL_VERSION}";

# curl prediction
curl -i -X POST -H "Content-Type: application/json" "http://localhost:9090/v1/models/${MODEL_NAME}:predict" -d "${BODY}";
```

### 4.B Serve Google AI Platform
```bash
# create model
gcloud ai-platform models create "${MODEL_NAME}" --regions "${REGION}" --project "${PROJECT_ID}";
# create version
gcloud ai-platform versions create "${JOB_NAME}" --project "${PROJECT_ID}" \
  --model "${MODEL_NAME}" \
  --framework "tensorflow" \
  --origin "${MODEL_BINARIES}" \
  --runtime-version "2.1" \
  --python-version "3.7";
```


### 5 Keras webapi

```bash
# build
docker build -t "gcr.io/${PROJECT_ID}/keras_webapi:${MODEL_VERSION}" -f "./keras_webapi/Dockerfile" "./keras_webapi";
# run app
docker run -it --rm --name keras_webapi -p 8080:8080 -e "GOOGLE_CLOUD_PROJECT=${PROJECT_ID}" \
  "gcr.io/${PROJECT_ID}/keras_webapi:${MODEL_VERSION}";
```

## 6. Test curls
```bash
# to AI Platform
curl -X POST -H 'Content-Type: application/json' "http://localhost:${PORT}/api/keras/${JOB_NAME}" -d "${BODY}";
# to Docker
curl -X POST -H 'Content-Type: application/json' "http://localhost:${PORT}/api/keras-host" -d "${BODY}";
```