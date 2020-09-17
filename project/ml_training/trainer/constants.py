import os

ENV = os.environ
MODEL_NAME = ENV['MODEL_NAME'] if 'MODEL_NAME' in ENV else 'testkeras'
EPOCHS = 10
CLASS_NAMES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
