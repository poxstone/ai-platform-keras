import os

import tensorflow as tf
import numpy as np
#import matplotlib.pyplot as plt

from trainer.constants import CLASS_NAMES, MODEL_NAME
from trainer.data import get_data 


train_images, train_labels, test_images, test_labels = get_data()

# load model foldder
model = tf.keras.models.load_model(MODEL_NAME)
# load test HDF5
#new_model = tf.keras.models.load_model(MODEL_NAME + '.h5')


# get prediction
# make prediction raw
probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

# set individuals images
i = 180
img_array = test_images[i:i+1]
predictions = probability_model.predict(img_array)

# prediction max range
label = CLASS_NAMES[np.argmax(predictions[0])]
print(label)
