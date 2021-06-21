import tensorflow as tf
import numpy as np
import PIL.Image
import re
from io import BytesIO
import base64
import os
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED' # Load compressed models from tensorflow_hub
import tensorflow_hub as tf_hub


class StyleTransfer(object):

  def __init__(self):
    print("Downloading and loading model...")
    #self.tf_hub_model = tf_hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    self.tf_hub_model = tf_hub.load('magenta_arbitrary-image-stylization-v1-256_2')
    print("Model loaded!")
  
  def transfer(self, style_image, content_image):
    return self.tf_hub_model(tf.constant(content_image), tf.constant(style_image))[0]

  @staticmethod
  def base64_to_tensor(base64_img):
    base64_payload = re.sub('^data:image/.+;base64,', '', base64_img)
    base64_payload_web_safe = base64_payload.replace('/', '_').replace('+', '-')
    file_as_string = tf.io.decode_base64(base64_payload_web_safe)
    return StyleTransfer.aux_to_tensor(file_as_string)

  @staticmethod
  def file_to_tensor(path_to_img):
    file_as_string = tf.io.read_file(path_to_img)
    return StyleTransfer.aux_to_tensor(file_as_string)

  @staticmethod
  def aux_to_tensor(img, max_dim=512):
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

  @staticmethod
  def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
      assert tensor.shape[0] == 1
      tensor = tensor[0]
    return PIL.Image.fromarray(tensor)

  @staticmethod
  def pillow_to_base64(img):
    buffered = BytesIO()
    img.convert('RGB').save(buffered, format='JPEG')
    return "data:image/jpg;base64," + base64.b64encode(buffered.getvalue()).decode('utf-8')
