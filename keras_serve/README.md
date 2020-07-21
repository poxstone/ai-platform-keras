# Serve model on docker

> **Note:** Previously execute ../README.md steps 1 and 2, enter to dir:
  </br> `cd "./keras_serve"`

## 3. Build and run container
- Build
```bash

docker build -t "gcr.io/${GOOGLE_CLOUD_PROJECT}/keras_serve:${MODEL_VERSION}" \
  --build-arg "MODEL_NAME=${MODEL_NAME}" \
  --build-arg "MODEL_LOCATION=./keras_training/keras_model/${MODEL_VERSION}/" \
  -f "Dockerfile" "../";
```
- Run
```bash
docker run -it --rm --name keras_serve --net host -e APP_PORT=9090 -p 9090:9090 -p 8500:8500 "gcr.io/${GOOGLE_CLOUD_PROJECT}/keras_serve:${MODEL_VERSION}";
```

## 4. Get prediction
- To google AI Platform
```bash
curl -i -X POST -H "Content-Type: application/json" "http://localhost:9090/v1/models/${MODEL_NAME}:predict" -d "${BODY}";
```
