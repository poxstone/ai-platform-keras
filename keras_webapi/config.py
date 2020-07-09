import os
import sys
import logging


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

ROOT_DIR = sys.path[0]
env = os.environ
PROJECT_ID = env['GOOGLE_CLOUD_PROJECT'] if 'GOOGLE_CLOUD_PROJECT' in env \
                                         else ''
GOOGLE_APPLICATION_CREDENTIALS = env['GOOGLE_APPLICATION_CREDENTIALS'] if \
                                'GOOGLE_APPLICATION_CREDENTIALS' in env else ''
MODEL = env['MODEL_NAME'] if 'MODEL_NAME' in env else 'keras_model'
APP_PORT = env['APP_PORT'] if 'APP_PORT' in env else 8080
LOCAL_ML_HOST = env['LOCAL_ML_HOST'] if 'LOCAL_ML_HOST' in env else 'localhost'
LOCAL_ML_PORT = env['LOCAL_ML_PORT'] if 'LOCAL_ML_PORT' in env else 9090
LOCAL_ML_NAME = env['LOCAL_ML_NAME'] if 'LOCAL_ML_NAME' in env else 'keras_model'
LOCAL_ML_VERSION = env['LOCAL_ML_VERSION'] if 'LOCAL_ML_VERSION' in env else '1'
