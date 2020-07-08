import googleapiclient.discovery
import requests
import json
from flask import Flask
from flask import request
from config import PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS, MODEL, APP_PORT, \
    LOCAL_ML_HOST, LOCAL_ML_PORT, LOCAL_ML_NAME, LOCAL_ML_VERSION
from utils import get_request_objects, standard_json_response
import logging

logging.info("PROJECT_ID={}, GOOGLE_APPLICATION_CREDENTIALS={}, MODEL={}, \
              APP_PORT={}".format(PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS,
                                  MODEL, APP_PORT))
app = Flask(__name__)


def predict_host_json(instances, version=LOCAL_ML_VERSION, model=LOCAL_ML_NAME):
    response = None
    body = {'instances': instances}
    ml_host = 'http://{}:{}/v{}/models/{}:predict'.format(LOCAL_ML_HOST,
                                                LOCAL_ML_PORT, version, model)
    try:
        res = requests.post(ml_host, json=body)
        response = json.loads(res.text)
    except Exception as e:
        logging.error(e)
        raise RuntimeError(response['error'])
    return response['predictions']


def predict_json(instances, version=None, model=MODEL, project=PROJECT_ID):
    # GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
    service = googleapiclient.discovery.build('ml', 'v1')
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)
    
    response = None

    try:
        response = service.projects().predict(name=name,
                                          body={'instances': instances}
                                         ).execute()
        logging.error(response)
    except Exception as e:
        logging.error('error getting api model: {}'.format(str(e)))

    if response and 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']


@app.route('/')
def path_root():
    return "ok"

@app.route('/api/keras/<version>', methods=['POST'])
def path_api(version):
    req_post = get_request_objects(request)['post']
    instances = req_post['instances'] if 'instances' in req_post else ''
    # businness logic
    prediction = predict_json(instances=instances, version=version)
    return standard_json_response('ok', data=prediction, to_json=False)

@app.route('/api/keras-host', methods=['POST'])
def path_host_api():
    req_post = get_request_objects(request)['post']
    instances = req_post['instances'] if 'instances' in req_post else ''
    # businness logic
    prediction = predict_host_json(instances=instances)
    return standard_json_response('ok', data=prediction, to_json=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_PORT)
