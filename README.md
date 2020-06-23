## keras model to AI Platform python 3.7
 - base [keras](https://github.com/GoogleCloudPlatform/cloudml-samples/tree/master/census/keras)


## install
```bash
python3.7 -m virtualenv venv;
source ./venv/bin/activate;

# install requirements
pip install -r requirements.txt;
# or
python setup.py install;
```

## variables
```bash
PROJECT="co-oortiz-internal";
BUCKER_NAME="co-oortiz-internal";
REGION="us-east1";
MODEL_NAME="keras_model";
JOB_NAME="keras_test_002";
MODEL_VERSION="${JOB_NAME}";
JOB_DIR="gs://${BUCKER_NAME}";
MODEL_BINARIES="${JOB_DIR}/${MODEL_NAME}/${JOB_NAME}/";
```


## send to AI Platform

```bash

# local python
python -m trainer.task --job-name $JOB_NAME --train-files $JOB_DIR --project "${PROJECT}";

# gcloud local
gcloud ai-platform local train --package-path trainer \
                             --module-name trainer.task \
                             -- \
                             --job-name $JOB_NAME --train-files $JOB_DIR;

# gcloud training
gcloud ai-platform jobs submit training $JOB_NAME \
                                    --stream-logs \
                                    --python-version 3.7 \
                                    --runtime-version 2.1 \
                                    --job-dir $JOB_DIR \
                                    --package-path trainer \
                                    --module-name trainer.task \
                                    --region ${REGION} \
                                    -- \
                                    --job-name $JOB_NAME --train-files $JOB_DIR \
                                    --verbosity DEBUG;
```

## create IA Platform model

```bash
# create model
gcloud ai-platform models create $MODEL_NAME --regions=$REGION --project "${PROJECT}";
# create version
gcloud ai-platform versions create "${MODEL_VERSION}" \
    --model "${MODEL_NAME}" \
    --framework "tensorflow" \
    --origin "${MODEL_BINARIES}" \
    --runtime-version "2.1" \
    --python-version "3.7";
```

## Test keras
- json to send test 1:
```json
gcloud ai-platform predict --model "${MODEL_NAME}" --version "${MODEL_VERSION}" --json-instances "model_doc/prediction_input.json";
```
- json to response prediction:
```json
{
  "predictions": [
    {
      "dense_1": [
        -9.610590934753418,
        -13.334138870239258,
        -11.145981788635254,
        -14.164958953857422,
        -13.480061531066895,
        -2.9960415363311768,
        -10.142991065979004,
        -1.643408179283142,
        -10.997992515563965,
        4.4618377685546875
      ]
    }
  ]
}
```

- json to send test 2:
```json
{"instances": [
  [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.05098039, 0.2627451 , 0.0 , 0.0 , 0.0 , 0.0 , 0.19607843, 0.14901961, 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.03137255, 0.47058824, 0.81960784, 0.88627451, 0.96862745, 0.92941176, 0.0 , 0.0 , 0.0 , 0.96862745, 0.93333333, 0.92156863, 0.6745098 , 0.28235294, 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.5372549 , 0.9372549 , 0.98823529, 0.95294118, 0.91764706, 0.89803922, 0.93333333, 0.95686275, 0.96470588, 0.94117647, 0.90196078, 0.90980392, 0.9372549 , 0.97254902, 0.98431373, 0.76078431, 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.4 , 0.0 , 0.90588235, 0.89411765, 0.89019608, 0.89411765, 0.91372549, 0.90196078, 0.90196078, 0.89803922, 0.89411765, 0.90980392, 0.90980392, 0.90588235, 0.89019608, 0.87843137, 0.98823529, 0.70196078, 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.91372549, 0.94509804, 0.89803922, 0.90588235, 0.0 , 0.0 , 0.93333333, 0.90588235, 0.89019608, 0.93333333, 0.96470588, 0.89411765, 0.90196078, 0.89019608, 0.91764706, 0.92156863, 0.89803922, 0.94509804, 0.07843137, 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.97254902, 0.94509804, 0.90588235, 0.0 , 0.58431373, 0.18431373, 0.98823529, 0.89411765, 0.0 , 0.94901961, 0.84705882, 0.93333333, 0.90980392, 0.0 , 0.89411765, 0.8627451 , 0.91764706, 0.98039216, 0.21176471, 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.94117647, 0.90980392, 0.0 , 0.05882353, 0.0 , 0.0 , 0.92941176, 0.74901961, 0.0 , 0.0 , 0.83921569, 0.0 , 0.05098039, 0.48235294, 0.0 , 0.91764706, 0.98823529, 0.44705882, 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.02352941, 0.0 , 0.93333333, 0.9372549 , 0.0 , 0.69411765, 0.0 , 0.0 , 0.0 , 0.0 , 0.50980392, 0.45490196, 0.18431373, 0.25490196, 0.16862745, 0.14509804, 0.0 , 0.9254902 , 0.97647059, 0.63529412, 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.1254902 , 0.0 , 0.9254902 , 0.96078431, 0.0 , 0.8 , 0.0 , 0.0 , 0.32941176, 0.0 , 0.14509804, 0.10980392, 0.12156863, 0.0 , 0.09803922, 0.05098039, 0.0 , 0.9254902 , 0.97647059, 0.78039216, 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.20784314, 0.0 , 0.9254902 , 0.98039216, 0.98039216, 0.90588235, 0.00784314, 0.0 , 0.08235294, 0.0 , 0.86666667, 0.0 , 0.9254902 , 0.21176471, 0.96078431, 0.77647059, 0.95294118, 0.93333333, 0.96078431, 0.8745098 , 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.31372549, 0.0 , 0.92941176, 0.98039216, 0.94117647, 0.0 , 0.0 , 0.0 , 0.15294118, 0.61568627, 0.0 , 0.0 , 0.84313725, 0.36862745, 0.07843137, 0.49411765, 0.0 , 0.92941176, 0.9372549 , 0.98039216, 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.39607843, 0.0 , 0.92156863, 0.99215686, 0.95686275, 0.95294118, 0.52156863, 0.54117647, 0.81568627, 0.0 , 0.78823529, 0.83921569, 0.0 , 0.90196078, 0.02745098, 0.68235294, 0.0 , 0.94117647, 0.93333333, 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.49411765, 0.0 , 0.91372549, 0.0 , 0.97254902, 0.91372549, 0.0 , 0.0 , 0.94117647, 0.90980392, 0.95294118, 0.95294118, 0.90588235, 0.98431373, 0.0 , 0.0 , 0.99607843, 0.95294118, 0.93333333, 0.0 , 0.01176471, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.57647059, 0.0 , 0.91372549, 0.97647059, 0.70980392, 0.95294118, 0.89019608, 0.87843137, 0.90196078, 0.91764706, 0.90196078, 0.90196078, 0.92156863, 0.89411765, 0.92156863, 0.87058824, 0.81176471, 0.0 , 0.9254902 , 0.0 , 0.1372549 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.63921569, 0.0 , 0.96078431, 0.86666667, 0.3372549 , 0.0 , 0.91372549, 0.91372549, 0.92156863, 0.9254902 , 0.91764706, 0.91764706, 0.91764706, 0.90980392, 0.94901961, 0.90588235, 0.49019608, 0.0 , 0.9254902 , 0.0 , 0.21568627, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.70980392, 0.99607843, 0.0 , 0.78431373, 0.27058824, 0.0 , 0.89411765, 0.90980392, 0.91764706, 0.92156863, 0.91764706, 0.91764706, 0.91372549, 0.92156863, 0.94509804, 0.92941176, 0.2745098 , 0.0 , 0.92156863, 0.96470588, 0.22352941, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.77254902, 0.96862745, 0.0 , 0.7372549 , 0.43137255, 0.0 , 0.87843137, 0.91372549, 0.91764706, 0.91764706, 0.91764706, 0.91764706, 0.91764706, 0.91764706, 0.94117647, 0.99215686, 0.27058824, 0.0 , 0.9254902 , 0.97254902, 0.30196078, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.78431373, 0.96470588, 0.0 , 0.58431373, 0.56862745, 0.0 , 0.8745098 , 0.92156863, 0.91764706, 0.92156863, 0.92156863, 0.92156863, 0.91764706, 0.92941176, 0.91372549, 0.0 , 0.18431373, 0.0 , 0.9372549 , 0.97647059, 0.38431373, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.8 , 0.95294118, 0.0 , 0.43529412, 0.67843137, 0.0 , 0.89019608, 0.92156863, 0.92156863, 0.9254902 , 0.92156863, 0.92156863, 0.92156863, 0.9372549 , 0.89803922, 0.0 , 0.0745098 , 0.89019608, 0.96470588, 0.97647059, 0.43137255, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.76862745, 0.94117647, 0.0 , 0.42745098, 0.83529412, 0.98039216, 0.89803922, 0.92156863, 0.92156863, 0.9254902 , 0.92156863, 0.92941176, 0.9254902 , 0.92941176, 0.88627451, 0.0 , 0.21568627, 0.79607843, 0.98431373, 0.96078431, 0.47058824, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.75294118, 0.95294118, 0.0 , 0.44705882, 0.90980392, 0.94117647, 0.90980392, 0.92156863, 0.92156863, 0.9254902 , 0.91764706, 0.92941176, 0.9254902 , 0.92156863, 0.89803922, 0.0 , 0.5254902 , 0.67058824, 0.98823529, 0.95686275, 0.5372549 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.74117647, 0.98431373, 0.0 , 0.60392157, 0.93333333, 0.91372549, 0.9254902 , 0.91764706, 0.92156863, 0.9254902 , 0.92156863, 0.93333333, 0.9254902 , 0.92156863, 0.90980392, 0.0 , 0.65098039, 0.49019608, 0.0 , 0.95294118, 0.55686275, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.71764706, 0.98823529, 0.0 , 0.67058824, 0.96862745, 0.90980392, 0.91764706, 0.91764706, 0.91372549, 0.91372549, 0.90980392, 0.91764706, 0.91372549, 0.91764706, 0.91372549, 0.94117647, 0.8745098 , 0.50196078, 0.0 , 0.94901961, 0.59215686, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.69803922, 0.95294118, 0.0 , 0.22352941, 0.93333333, 0.94509804, 0.93333333, 0.93333333, 0.93333333, 0.92941176, 0.9254902 , 0.92941176, 0.92941176, 0.94117647, 0.92941176, 0.99607843, 0.69019608, 0.20392157, 0.0 , 0.9372549 , 0.61568627, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.7372549 , 0.94117647, 0.98039216, 0.24313725, 0.85490196, 0.0 , 0.8627451 , 0.87058824, 0.87058824, 0.87058824, 0.8745098 , 0.8745098 , 0.87843137, 0.87058824, 0.85490196, 0.0 , 0.60392157, 0.1254902 , 0.0 , 0.9254902 , 0.7372549 , 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.50980392, 0.96078431, 0.94901961, 0.09411765, 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.13333333, 0.94901961, 0.95686275, 0.52941176, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.29803922, 0.0 , 0.97647059, 0.08627451, 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.15294118, 0.97647059, 0.0 , 0.48235294, 0.0 , 0.0 , 0.0 ],
  [0.0 , 0.0 , 0.0 , 0.0 , 0.19215686, 0.80392157, 0.77254902, 0.04313725, 0.0 , 0.01568627, 0.00392157, 0.00784314, 0.00784314, 0.00784314, 0.00784314, 0.00784314, 0.00784314, 0.00784314, 0.00784314, 0.01176471, 0.0 , 0.01176471, 0.68235294, 0.74117647, 0.2627451 , 0.0 , 0.0 , 0.0 ]
]}
```
- json to response prediction:
```json
{
  "predictions": [
    {
      "dense_1": [
        1.8627415895462036,
        -13.13156795501709,
        9.79440975189209,
        -8.527874946594238,
        -0.24184119701385498,
        -9.566632270812988,
        4.248584747314453,
        -28.790557861328125,
        -4.069375514984131,
        -19.317222595214844
      ]
    }
  ]
}
```