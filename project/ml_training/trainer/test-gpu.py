import tensorflow.compat.v1 as tf
# test gpu
tf.Session(config=tf.ConfigProto(log_device_placement=True))
