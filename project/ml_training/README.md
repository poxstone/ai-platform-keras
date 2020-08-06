## keras model to AI Platform python 3.7

> **Note:** Previously execute ../README.md steps 1 and 2 and:
  </br> `cd "./ml_training"`
* **Original:** [keras census](https://github.com/GoogleCloudPlatform/cloudml-samples/tree/master/census/keras)


## 1. Install (optional)
Setup is builder python (./build and ./dist)
```bash
python setup.py install;
```


## 2. Send to AI Platform

### 2.1 Train local
```bash
python -m trainer.task --job-version "${MODEL_VERSION}" --trainded-dir "${BUCKET_NAME}";
```
#### 2.1.2 Test local
```bash
python -m trainer.task --job-version "${MODEL_VERSION}" --is-test "true" --img-index 0;
```

### 2.2 Train local with AI Platform
```bash
gcloud ai-platform local train --package-path trainer \
  --module-name trainer.task \
  -- \
  --job-version "${MODEL_VERSION}" --trainded-dir "${BUCKET_NAME}";
```

### 2.3 Send to AI Platform to train
```bash
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

### 2.4 Send ___container___ to AI Platform to train
- Build container
```bash
docker build -t "gcr.io/${GOOGLE_CLOUD_PROJECT}/${MODEL_NAME}:${MODEL_VERSION}" \
  --build-arg "MODEL_VERSION=${MODEL_VERSION}" \
  --build-arg "JOB_DIR=${JOB_DIR}" -f "Dockerfile" "./";
```

- Run container local
```bash
docker run -it --rm "gcr.io/${GOOGLE_CLOUD_PROJECT}/${MODEL_NAME}:${MODEL_VERSION}";
```

- Upload images to Google Container Registry
```bash
# authorize docker
gcloud auth configure-docker;
# push container
docker push "gcr.io/${GOOGLE_CLOUD_PROJECT}/${MODEL_NAME}:${MODEL_VERSION}";

# optional build on GCP and store in GCR
export DOCKERFILE="./Dockerfile";
grep "${DOCKERFILE}" -ne "^ARG MODEL_VERSION" | awk -F ":" '{print($1)}' | xargs -I {} sed -i {}'s/.\+/ARG MODEL_VERSION="'${MODEL_VERSION}'"/' "${DOCKERFILE}";
grep "${DOCKERFILE}" -ne "^ARG JOB_DIR" | awk -F ":" '{print($1)}' | xargs -I {} sed -i {}'s/.\+/ARG JOB_DIR="'${BUCKET_NAME}'"/' "${DOCKERFILE}";
gcloud builds submit --tag "gcr.io/${GOOGLE_CLOUD_PROJECT}/${MODEL_NAME}:${MODEL_VERSION}" "./"  --project "${GOOGLE_CLOUD_PROJECT}";
```

- Train container on AI Platform
```bash
gcloud ai-platform jobs submit training "${JOB_NAME}" --project "${GOOGLE_CLOUD_PROJECT}" \
  --stream-logs \
  --region "${REGION}" \
  --master-image-uri "gcr.io/${GOOGLE_CLOUD_PROJECT}/${MODEL_NAME}:${MODEL_VERSION}" \
  -- \
  --job-version "${MODEL_VERSION}" --trainded-dir "${BUCKET_NAME}" \
  --verbosity DEBUG;
```

## 3. Create AI Platform model and version
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
```


## 3. Test Model

> **Note** The arrays images is taked from "keras.datasets.fashion_mnist" test_images, index 0 and 1
- json to send test 1 use page(use UI):
  - https://console.cloud.google.com/ai-plaecho tform/models/${MODEL_NAME}/versions/${JOB_NAME}/test-and-use?project=${GOOGLE_CLOUD_PROJECT}
```bash
# not works, use UI!
gcloud ai-platform predict --model "${MODEL_NAME}" --version "${JOB_NAME}" \
  --json-instances "${BODY_PATH}" --project "${GOOGLE_CLOUD_PROJECT}";
```
- json to response prediction:
```json
{
  "predictions": [
    {
      "dense_1": [
        -5.473412036895752,
        -7.7068190574646,
        -7.146913528442383,
        -6.737424373626709,
        -6.216702938079834,
        2.6814448833465576,
        -4.87260103225708,
        3.713648796081543,
        0.6895899772644043,
        5.182033061981201
      ]
    }
  ]
}
```

- json to send test 2:
```json
{"instances": [
  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05098039, 0.2627451 , 0.0, 0.0, 0.0, 0.0, 0.19607843, 0.14901961, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03137255, 0.47058824, 0.81960784, 0.88627451, 0.96862745, 0.92941176, 0.0, 0.0, 0.0, 0.96862745, 0.93333333, 0.92156863, 0.6745098 , 0.28235294, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5372549 , 0.9372549 , 0.98823529, 0.95294118, 0.91764706, 0.89803922, 0.93333333, 0.95686275, 0.96470588, 0.94117647, 0.90196078, 0.90980392, 0.9372549 , 0.97254902, 0.98431373, 0.76078431, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.0, 0.4 , 0.0, 0.90588235, 0.89411765, 0.89019608, 0.89411765, 0.91372549, 0.90196078, 0.90196078, 0.89803922, 0.89411765, 0.90980392, 0.90980392, 0.90588235, 0.89019608, 0.87843137, 0.98823529, 0.70196078, 0.0, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.0, 0.91372549, 0.94509804, 0.89803922, 0.90588235, 0.0, 0.0, 0.93333333, 0.90588235, 0.89019608, 0.93333333, 0.96470588, 0.89411765, 0.90196078, 0.89019608, 0.91764706, 0.92156863, 0.89803922, 0.94509804, 0.07843137, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.0, 0.97254902, 0.94509804, 0.90588235, 0.0, 0.58431373, 0.18431373, 0.98823529, 0.89411765, 0.0, 0.94901961, 0.84705882, 0.93333333, 0.90980392, 0.0, 0.89411765, 0.8627451 , 0.91764706, 0.98039216, 0.21176471, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.94117647, 0.90980392, 0.0, 0.05882353, 0.0, 0.0, 0.92941176, 0.74901961, 0.0, 0.0, 0.83921569, 0.0, 0.05098039, 0.48235294, 0.0, 0.91764706, 0.98823529, 0.44705882, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.02352941, 0.0, 0.93333333, 0.9372549 , 0.0, 0.69411765, 0.0, 0.0, 0.0, 0.0, 0.50980392, 0.45490196, 0.18431373, 0.25490196, 0.16862745, 0.14509804, 0.0, 0.9254902 , 0.97647059, 0.63529412, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.1254902 , 0.0, 0.9254902 , 0.96078431, 0.0, 0.8 , 0.0, 0.0, 0.32941176, 0.0, 0.14509804, 0.10980392, 0.12156863, 0.0, 0.09803922, 0.05098039, 0.0, 0.9254902 , 0.97647059, 0.78039216, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.20784314, 0.0, 0.9254902 , 0.98039216, 0.98039216, 0.90588235, 0.00784314, 0.0, 0.08235294, 0.0, 0.86666667, 0.0, 0.9254902 , 0.21176471, 0.96078431, 0.77647059, 0.95294118, 0.93333333, 0.96078431, 0.8745098 , 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.31372549, 0.0, 0.92941176, 0.98039216, 0.94117647, 0.0, 0.0, 0.0, 0.15294118, 0.61568627, 0.0, 0.0, 0.84313725, 0.36862745, 0.07843137, 0.49411765, 0.0, 0.92941176, 0.9372549 , 0.98039216, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.39607843, 0.0, 0.92156863, 0.99215686, 0.95686275, 0.95294118, 0.52156863, 0.54117647, 0.81568627, 0.0, 0.78823529, 0.83921569, 0.0, 0.90196078, 0.02745098, 0.68235294, 0.0, 0.94117647, 0.93333333, 0.0, 0.0, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.49411765, 0.0, 0.91372549, 0.0, 0.97254902, 0.91372549, 0.0, 0.0, 0.94117647, 0.90980392, 0.95294118, 0.95294118, 0.90588235, 0.98431373, 0.0, 0.0, 0.99607843, 0.95294118, 0.93333333, 0.0, 0.01176471, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.57647059, 0.0, 0.91372549, 0.97647059, 0.70980392, 0.95294118, 0.89019608, 0.87843137, 0.90196078, 0.91764706, 0.90196078, 0.90196078, 0.92156863, 0.89411765, 0.92156863, 0.87058824, 0.81176471, 0.0, 0.9254902 , 0.0, 0.1372549 , 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.63921569, 0.0, 0.96078431, 0.86666667, 0.3372549 , 0.0, 0.91372549, 0.91372549, 0.92156863, 0.9254902 , 0.91764706, 0.91764706, 0.91764706, 0.90980392, 0.94901961, 0.90588235, 0.49019608, 0.0, 0.9254902 , 0.0, 0.21568627, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.70980392, 0.99607843, 0.0, 0.78431373, 0.27058824, 0.0, 0.89411765, 0.90980392, 0.91764706, 0.92156863, 0.91764706, 0.91764706, 0.91372549, 0.92156863, 0.94509804, 0.92941176, 0.2745098 , 0.0, 0.92156863, 0.96470588, 0.22352941, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.77254902, 0.96862745, 0.0, 0.7372549 , 0.43137255, 0.0, 0.87843137, 0.91372549, 0.91764706, 0.91764706, 0.91764706, 0.91764706, 0.91764706, 0.91764706, 0.94117647, 0.99215686, 0.27058824, 0.0, 0.9254902 , 0.97254902, 0.30196078, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.78431373, 0.96470588, 0.0, 0.58431373, 0.56862745, 0.0, 0.8745098 , 0.92156863, 0.91764706, 0.92156863, 0.92156863, 0.92156863, 0.91764706, 0.92941176, 0.91372549, 0.0, 0.18431373, 0.0, 0.9372549 , 0.97647059, 0.38431373, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.8 , 0.95294118, 0.0, 0.43529412, 0.67843137, 0.0, 0.89019608, 0.92156863, 0.92156863, 0.9254902 , 0.92156863, 0.92156863, 0.92156863, 0.9372549 , 0.89803922, 0.0, 0.0745098 , 0.89019608, 0.96470588, 0.97647059, 0.43137255, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.76862745, 0.94117647, 0.0, 0.42745098, 0.83529412, 0.98039216, 0.89803922, 0.92156863, 0.92156863, 0.9254902 , 0.92156863, 0.92941176, 0.9254902 , 0.92941176, 0.88627451, 0.0, 0.21568627, 0.79607843, 0.98431373, 0.96078431, 0.47058824, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.75294118, 0.95294118, 0.0, 0.44705882, 0.90980392, 0.94117647, 0.90980392, 0.92156863, 0.92156863, 0.9254902 , 0.91764706, 0.92941176, 0.9254902 , 0.92156863, 0.89803922, 0.0, 0.5254902 , 0.67058824, 0.98823529, 0.95686275, 0.5372549 , 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.74117647, 0.98431373, 0.0, 0.60392157, 0.93333333, 0.91372549, 0.9254902 , 0.91764706, 0.92156863, 0.9254902 , 0.92156863, 0.93333333, 0.9254902 , 0.92156863, 0.90980392, 0.0, 0.65098039, 0.49019608, 0.0, 0.95294118, 0.55686275, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.71764706, 0.98823529, 0.0, 0.67058824, 0.96862745, 0.90980392, 0.91764706, 0.91764706, 0.91372549, 0.91372549, 0.90980392, 0.91764706, 0.91372549, 0.91764706, 0.91372549, 0.94117647, 0.8745098 , 0.50196078, 0.0, 0.94901961, 0.59215686, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.69803922, 0.95294118, 0.0, 0.22352941, 0.93333333, 0.94509804, 0.93333333, 0.93333333, 0.93333333, 0.92941176, 0.9254902 , 0.92941176, 0.92941176, 0.94117647, 0.92941176, 0.99607843, 0.69019608, 0.20392157, 0.0, 0.9372549 , 0.61568627, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.7372549 , 0.94117647, 0.98039216, 0.24313725, 0.85490196, 0.0, 0.8627451 , 0.87058824, 0.87058824, 0.87058824, 0.8745098 , 0.8745098 , 0.87843137, 0.87058824, 0.85490196, 0.0, 0.60392157, 0.1254902 , 0.0, 0.9254902 , 0.7372549 , 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.50980392, 0.96078431, 0.94901961, 0.09411765, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13333333, 0.94901961, 0.95686275, 0.52941176, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.29803922, 0.0, 0.97647059, 0.08627451, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15294118, 0.97647059, 0.0, 0.48235294, 0.0, 0.0, 0.0 ],
  [0.0, 0.0, 0.0, 0.0, 0.19215686, 0.80392157, 0.77254902, 0.04313725, 0.0, 0.01568627, 0.00392157, 0.00784314, 0.00784314, 0.00784314, 0.00784314, 0.00784314, 0.00784314, 0.00784314, 0.00784314, 0.01176471, 0.0, 0.01176471, 0.68235294, 0.74117647, 0.2627451 , 0.0, 0.0, 0.0 ]
]}
```
- json to response prediction:
```json
{
  "predictions": [
    {
      "dense_1": [
        -0.14419423043727875,
        -6.030039310455322,
        6.623904228210449,
        -0.08658134937286377,
        0.470222145318985,
        -4.250898838043213,
        3.3397421836853027,
        -8.513681411743164,
        -3.0367467403411865,
        -8.227275848388672
      ]
    }
  ]
}
```