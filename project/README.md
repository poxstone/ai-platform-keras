# Api web model to predict

> **Note:** Previously execute ../README.md steps 1 and 2, enter to dir:
  </br> `cd "./keras_webapi"`


## 1. Install (optional)
Setup is builder python (./build and ./dist)
```bash
python setup.py install;
```

## 2. Run code
```bash
# previous load enviroment variables with ../README.md steps 1 and 2
python main.py;
```

## 3. Build and run container
- Build
```bash
docker build -t "gcr.io/${GOOGLE_CLOUD_PROJECT}/keras_webapi:${MODEL_VERSION}" -f "Dockerfile" "./";
```
- Run
```bash
docker run -it --rm --name keras_webapi -p 8080:8080 -e "GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" \
  "gcr.io/${GOOGLE_CLOUD_PROJECT}/keras_webapi:${MODEL_VERSION}";
```

## 4. Get prediction
- To google AI Platform
```bash
curl -X POST -H 'Content-Type: application/json' "http://localhost:${PORT}/api/keras/${JOB_NAME}" -d "${BODY}";
```

- To docker server
```bash
curl -X POST -H 'Content-Type: application/json' "http://localhost:${PORT}/api/keras-host" -d "${BODY}";
```

## Tests
- 
```bash
# install test tools
pip install coverage pytest;

# create .coverage state file with tests
coverage run -m pytest tests/test_main.py;

# generate xml
coverage xml;
```