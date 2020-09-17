import numpy as np
import tensorflow as tf
from tensorflow import keras


def clothes_model():
    MODEL_NAME = 'clothes_model'  # folder dir
    MODEL_NAME = 'clothes_model/clothes.h5'  # h5 dir
    IMG_INDEX = 1
    CLASS_NAMES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    # load dataset
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()


    # load model and make prediction raw
    model = tf.keras.models.load_model(MODEL_NAME)
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])


    # set individuals images
    i = int(IMG_INDEX)
    img_array = test_images[i:i+1]  # to stact  img_array[0]
    predictions = probability_model.predict(img_array)

    # prediction max range
    label = CLASS_NAMES[np.argmax(predictions[0])]
    print("Predictions: {}".format(str(predictions[0])))
    print("Label: {}".format(label))

clothes_model()