import base64
import os

ENCODING = 'utf-8'
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
IMAGE_JPG = os.path.join(DIR_PATH, 'resources/pyramid-logo.jpg')
IMAGE_PNG = os.path.join(DIR_PATH, 'resources/pyramid-logo.png')

byte_content = ''
with open(IMAGE_PNG, 'rb') as image_file:
    byte_content = image_file.read()

base64_bytes = base64.b64encode(byte_content)
IMAGE_PNG_ENCODED = base64_bytes
IMAGE_PNG_ENCODED_STRING = base64_bytes.decode(ENCODING)

IMAGE_JPG_ENCODED = ''
with open(IMAGE_JPG, 'rb') as image_file:
    byte_content = image_file.read()

base64_bytes_jpg = base64.b64encode(byte_content)
IMAGE_JPG_ENCODED = base64_bytes_jpg
IMAGE_JPG_ENCODED_STRING = base64_bytes_jpg.decode(ENCODING)
