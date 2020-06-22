import os
import sys

ROOT_DIR = sys.path[0]
env = os.environ
PROJECT_ID = env['GOOGLE_CLOUD_PROJECT'] if 'GOOGLE_CLOUD_PROJECT' in env \
                                         else ''
GOOGLE_APPLICATION_CREDENTIALS = env['GOOGLE_APPLICATION_CREDENTIALS'] if \
                                'GOOGLE_APPLICATION_CREDENTIALS' in env else ''
MODEL = env['MODEL_NAME'] if 'MODEL_NAME' in env else 'keras_model'
PORT = env['PORT'] if 'PORT' in env else 8080
