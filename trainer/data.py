
from tensorflow import keras

# Load tensorflow examples Fashion MNIST

def get_data():
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    # ndarray

    # scale images or divide into 255
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    return train_images, train_labels, test_images, test_labels
