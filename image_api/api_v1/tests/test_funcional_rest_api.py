import json
import transaction
import unittest

from image_api.api_v1.models import Image
from image_api.api_v1.tests import BaseTest
from image_api.api_v1.utils import extract_metadata
from image_api.core.models import Base
from image_api.core.models import get_engine
from image_api.core.models import get_tm_session

from .settings import IMAGE_JPG_ENCODED_STRING
from .settings import IMAGE_PNG_ENCODED_STRING

BASE_API_URL = '/api/v1'


class ImageRestApiTests(unittest.TestCase):

    api_url_list = '/api/v1/image/'
    api_url_detail = '/api/v1/image/{0}/'

    def setUp(self):
        settings = {
            'sqlalchemy.url': 'sqlite:///test-db.sqlite'
        }
        from image_api import main_test
        app, config = main_test({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

        # session_factory = config.registry.get('dbsession_factory')
        # self.dbsession = get_tm_session(session_factory, transaction.manager)

        self.engine = get_engine(settings)
        self.init_database()

    def init_database(self):
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        transaction.abort()
        Base.metadata.drop_all(self.engine)

    def test_root(self):
        response = self.testapp.get('/')

        assert b'Working' in response.body
        assert response.status_code == 200

    def test_create_image(self):
        json_body = {
            'image': IMAGE_JPG_ENCODED_STRING,
            'name': 'image2.jpg'
        }
        response = self.testapp.post(self.api_url_list, json.dumps(json_body))

        assert response.status_code == 201

    def test_get_image_by_id(self):
        json_body = {
            'image': IMAGE_JPG_ENCODED_STRING,
        }
        response = self.testapp.post(self.api_url_list, json.dumps(json_body))

        # assert self.dbsession.query(Image).count() == 1

        json_resp = json.loads(response.body)
        image_id = json_resp.get('reponse').get('id')
        url = self.api_url_detail.format(image_id)
        print(url)
        response = self.testapp.get(url)
        assert response.status_code == 200

    def test_get_image_list(self):
        json = {'image': ''}
        response = self.testapp.get(self.api_url_list, json)

        assert response.status_code == 200
