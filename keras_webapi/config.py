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
