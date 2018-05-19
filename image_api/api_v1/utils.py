import base64
import magic
import os
import re


class SourceFile(object):
    BUFFER = 0
    FILE = 1

EXTENSIONS = {
    'png': 'png',
    'jpeg': 'jpg'
}


def extract_metadata(image):
    """
        Receives a image file
    """
    size = os.path.getsize(image)
    mime = magic.from_file(image, mime=True)
    text = magic.from_file(image)

    data = {'mime': mime, 'size': size, 'length': 0, 'width': 0}

    if 'image' in mime:
        format = mime.replace('image/', '')

        data.update(file_type='image')
        data.update(format=format)
        data.update(extension=EXTENSIONS.get(format, ''))

    text_cleaned = ''.join(text.split(' ')).lower()
    p = re.search('(\d*)x(\d*)', text_cleaned)
    if p:
        data.update(length=int(p.group(1)))
        data.update(width=int(p.group(2)))
    return data


def base64decode(image):
    image = image.encode('utf-8')
    return base64.b64decode(image)


def store_image(image):
    pass


def retrive_image(image):
    pass
