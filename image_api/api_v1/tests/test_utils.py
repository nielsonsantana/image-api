import unittest

from .settings import DIR_PATH
from .settings import IMAGE_JPG
from .settings import IMAGE_JPG_ENCODED
from .settings import IMAGE_PNG
from .settings import IMAGE_PNG_ENCODED


from image_api.api_v1.utils import extract_metadata


class ImageUtilsTests(unittest.TestCase):

    def test_extract_metadata_png(self):
        data = extract_metadata(IMAGE_PNG)

        assert data
        assert 'format' in data.keys()
        assert 'size' in data.keys()
        assert 'length' in data.keys()
        assert 'width' in data.keys()

        assert data['format'] == 'png'
        assert data['file_type'] == 'image'

    def test_extract_metadata_jpg(self):
        data = extract_metadata(IMAGE_JPG)

        assert data
        assert 'format' in data.keys()
        assert 'size' in data.keys()
        assert 'length' in data.keys()
        assert 'width' in data.keys()

        assert data['format'] == 'jpeg'
        assert data['file_type'] == 'image'
