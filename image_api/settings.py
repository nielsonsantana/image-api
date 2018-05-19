import os

from os.path import dirname
from os.path import join


def get_media_dir():
    root_dir = dirname(dirname(os.path.realpath(__file__)))
    media = join(root_dir, 'media')
    return media
