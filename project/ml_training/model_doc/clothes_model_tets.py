import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
import cv2 as cv


def clothes_model():
    MODEL_NAME = 'model_test'  # folder dir
    MODEL_NAME = '{}/model.h5'.format(MODEL_NAME)  # h5 dir
    IMG_INDEX = 1
    CLASS_NAMES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    # load dataset
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()


    # load model and make prediction raw
    model = tf.keras.models.load_model(MODEL_NAME)

    model.summary()
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])


    # set individuals images
    i = int(IMG_INDEX)
    img_array = test_images[i:i+1]  # to stact  img_array[0]
    predictions = probability_model.predict(img_array)

    # prediction max range
    label = CLASS_NAMES[np.argmax(predictions[0])]
    print("Predictions: {}".format(str(predictions[0])))
    print("Label: {}".format(label))


def minist_classification():
    MODEL_NAME = 'walkthrough'
    model = tf.keras.models.load_model(MODEL_NAME)
    predict_dataset = tf.convert_to_tensor([
        [5.1, 3.3, 1.7, 0.5,],
        [5.9, 3.0, 4.2, 1.5,],
        [6.9, 3.1, 5.4, 2.1]
    ])
    predictions = model(predict_dataset, training=False)

    print(str(predictions))


def walthrough_classification():
    CLASS_NAMES = ['Shoe', 'Movil', 'Bed', 'Book', 'Sofa']

    n_model = tf.keras.models.load_model('model_minist/model.h5')
    
    img_array = plt.imread('{}/image2.jpg'.format('./model_minist'))
    #im = cv.imread('{}/image2.jpg'.format('./model'))
    #im = cv.imread('IMG/cel.png')
    #img = (np.expand_dims(im/255.0,0))
    #img = img.tolist()

    preds = n_model.predict(img_array)

    
    #n_model = tf.keras.models.load_model('my_model', compile=True)
    #n_model.evaluate(val_dataset, steps=val_data.shape[0] // batch_size)

    # load model and make prediction raw
    #probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])


    # set individuals images
    #preds = model.predict(img_array)

    # prediction max range
    print("prediction: {}".format(preds))

#another_model()
#clothes_model()
walthrough_classification()


###
#n_model = tf.keras.models.load_model('model')

#gln._model.load_weights('model.h5')
#n_model = tf.keras.models.load_model('my_model', compile=True)
