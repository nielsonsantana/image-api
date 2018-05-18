import json
import unittest

from image_api.api_v1.models import Image
from image_api.api_v1.tests import BaseTest
from image_api.api_v1.utils import extract_metadata

from .settings import IMAGE_JPG_ENCODED
from .settings import IMAGE_JPG_ENCODED_STRING
from .settings import IMAGE_PNG_ENCODED
from .settings import IMAGE_PNG_ENCODED_STRING

BASE_API_URL = '/api/v1'


class ImageRestApiTests(unittest.TestCase):

    api_url_list = '/api/v1/image/'
    api_url_detail = '/api/v1/image/{0}/'

    def setUp(self):
        settings = {
            'sqlalchemy.url': 'sqlite:///:memory:'
        }
        from image_api import main
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        response = self.testapp.get('/')

        assert b'Working' in response.body
        assert response.status_int == 200

    def test_create_image(self):
        json_body = {
            'image': IMAGE_JPG_ENCODED_STRING,
            'name': 'image2.jpg'
        }
        response = self.testapp.post(self.api_url_list, json.dumps(json_body))

        print(response.body)
        assert response.status_int == 201

    def test_get_image_by_id(self):
        json = {'image': IMAGE_JPG_ENCODED}
        response = self.testapp.get(self.api_url_detail, json)

        print(response.body)
        assert response.status_int == 200

    def test_get_image_list(self):
        json = {'image': IMAGE_JPG_ENCODED}
        response = self.testapp.get(self.api_url_list, json)

        assert response.status_int == 200
