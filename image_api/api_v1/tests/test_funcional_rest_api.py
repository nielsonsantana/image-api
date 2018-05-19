import json
import transaction
import unittest

from image_api.api_v1.models import Image
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

        session_factory = config.registry.get('dbsession_factory')
        self.dbsession = get_tm_session(session_factory, transaction.manager)

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
        json_body = json.dumps({
            'image': IMAGE_JPG_ENCODED_STRING,
            'name': 'image2.jpg'
        })
        response = self.testapp.post(self.api_url_list, json_body)

        assert response.status_code == 201

        query = self.dbsession.query(Image)
        assert query.count() == 1
        image = query.first()
        assert image.format == 'jpeg'

    def test_get_image_by_id(self):
        json_body = json.dumps({
            'image': IMAGE_JPG_ENCODED_STRING,
        })
        response = self.testapp.post(self.api_url_list, json_body)

        json_resp = json.loads(response.body)
        image_id = json_resp.get('content').get('id')
        url = self.api_url_detail.format(image_id)
        response = self.testapp.get(url)
        assert response.status_code == 200

    def test_get_image_list(self):
        json_body_png = json.dumps({
            'image': IMAGE_PNG_ENCODED_STRING,
        })
        response_png = self.testapp.post(self.api_url_list, json_body_png)
        json_body_jpg = json.dumps({
            'image': IMAGE_JPG_ENCODED_STRING,
        })
        response_jpg = self.testapp.post(self.api_url_list, json_body_jpg)

        response = self.testapp.get(self.api_url_list)

        assert response.status_code == 200

        image_list = response.json['content']

        assert len(image_list) == 2

        id_list = [obj.get('id') for obj in image_list]

        assert response_png.json['content'].get('id') in id_list
        assert response_jpg.json['content'].get('id') in id_list
