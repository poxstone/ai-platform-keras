# TensorFlow and tf.keras
#import logging
import os
import random
import re
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.lib.io import file_io

try:
    from trainer import constants  # docker
    from trainer.data import get_data
except ImportError:
    import constants  # local for debug
    from data import get_data


random.seed(666)

def save_folder(job_version, save_path, gs_path, path=None):
    if not gs_path.endswith('/'):
        gs_path = '{}/'.format(gs_path)
    # save cloud storage
    if not path:
        path = '{}'.format(save_path)
    
    list_dir = tf.io.gfile.listdir(path)
    if not list_dir:
        return False

    for file in list_dir:
        concat_name = '{}/{}'.format(path, file)
        if tf.io.gfile.isdir(concat_name):
            save_folder(job_version=job_version, save_path=save_path,
                        gs_path=gs_path, path=concat_name)
        else:
            with file_io.FileIO(concat_name, mode='rb') as input_f:
                gs_write = os.path.join(gs_path, concat_name)
                print("gs_write: " + gs_write)
                with file_io.FileIO(gs_write, mode='w+') as fp:
                    fp.write(input_f.read())
    return True


def training(args):
    # Clear and set parameters
    JOB_VERSION = args.job_version[0]
    GS_BUCKET = re.sub('/$', '', args.trainded_dir[0])
    if not GS_BUCKET.startswith('gs://'):
        GS_BUCKET = 'gs://{}'.format(GS_BUCKET)
    
    # load test dataset
    train_images, train_labels, test_images, test_labels = get_data()

    # Config layers model
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10)
    ])

    # setup compile model
    model.compile(optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])

    # train model
    model.fit(train_images, train_labels, epochs=constants.EPOCHS)

    # evaluate model get loss and accurancy
    #test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)

    # save model for AI Platform
    save_path = '{}/{}'.format(constants.MODEL_NAME, JOB_VERSION)
    try:
        os.mkdir(constants.MODEL_NAME)
    except:
        pass

    print('----- {}'.format(save_path))
    # savelocal
    model.save("{}.h5".format(save_path))
    tf.keras.models.save_model(model, save_path, overwrite=True,
        include_optimizer=True, save_format=None, signatures=None, options=None)
    
    save_folder(job_version=JOB_VERSION, save_path=save_path, gs_path=GS_BUCKET)
    export_path = '{}/{}'.format(GS_BUCKET, save_path)
    print(export_path)

    # do prediction test
    evaluate(args)
    
    return export_path


def evaluate(args):
    import numpy as np

    JOB_VERSION = args.job_version[0]
    if args.img_index and len(args.img_index):
        IMG_INDEX = args.img_index[0]
    else:
        IMG_INDEX = 0
    
    dir_model = os.path.join(constants.MODEL_NAME, JOB_VERSION)
    model = tf.keras.models.load_model(dir_model)
    
    # make prediction raw
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

    # load dataset
    train_images, train_labels, test_images, test_labels = get_data()

    # set individuals images
    i = int(IMG_INDEX)
    img_array = test_images[i:i+1]  # to stact  img_array[0]
    predictions = probability_model.predict(img_array)

    # prediction max range
    label = constants.CLASS_NAMES[np.argmax(predictions[0])]
    print("Predictions: {}".format(str(predictions[0])))
    print("Label: {}".format(label))
