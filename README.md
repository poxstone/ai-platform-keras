# IA Platform project (keras sample)

- keras training
- keras serving
- keras web app api consumer AI Platform

## Install enviroment python
```bash
python3 -m virtualenv venv;
source venv/bin/activate;
# install for weapp
pip install -r keras_webapi/requirements.txt;
# install for model
pip install -r keras_model/requiremetns.txt;
# install for server
pip install -r keras_serve/requirements.txt;
```

## Variables
```bash
source ../variables.sh;
```

## Build containers
```bash
# keras webapi
docker build -t gcr.io/${PROJECT_ID}/keras_webapi:${MODEL_VERSION} -f Dockerfile_webapi ./;
docker run -itd --rm --name keras_webapi -p 8080:8080 -e "GOOGLE_CLOUD_PROJECT=${PROJECT_ID}" gcr.io/${PROJECT_ID}/keras_webapi:${MODEL_VERSION};

# keras training
docker build -t gcr.io/${PROJECT_ID}/keras_training:${MODEL_VERSION} -f Dockerfile_training ./;
docker run -it --rm gcr.io/${PROJECT_ID}/keras_training:${MODEL_VERSION};

# gcloud training
gcloud ai-platform jobs submit training $JOB_NAME \
    --stream-logs \
    --master-image-uri gcr.io/${PROJECT_ID}/keras_training:${MODEL_VERSION} \
    --job-dir $JOB_DIR \
    --region ${REGION} \
    -- \
    --job-name $JOB_NAME --train-files $JOB_DIR \
    --verbosity DEBUG;

# keras model serving docker
docker build -t gcr.io/${PROJECT_ID}/keras_serve:${MODEL_VERSION} --build-arg APP_VERSION=2 -f Dockerfile_serve ./ --;
# run serve
docker run -it --rm --name keras_serve --net host -p 8080:9090 -p 8500:8500 gcr.io/${PROJECT_ID}/keras_serve:${MODEL_VERSION};
# curl prediction
curl -i -X POST -H "Content-Type: application/json" "http://localhost:8080/v1/models/keras_model:predict" -d "${BODY}";
```
