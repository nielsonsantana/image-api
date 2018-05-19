import json
import transaction

from pyramid import testing

from image_api.api_v1.models import Image
from image_api.api_v1.tests import BaseTest
from image_api.api_v1.views import image_detail
from image_api.api_v1.views import image_list

from .settings import IMAGE_JPG_ENCODED_STRING
from .settings import IMAGE_PNG_ENCODED_STRING


def dummy_request(dbsession=None, **kwargs):
    return testing.DummyRequest(dbsession=dbsession, **kwargs)


class ImageViewsTests(BaseTest):

    def setUp(self):
        super(ImageViewsTests, self).setUp()
        self.init_database()

    def test_register_image_png(self):
        params = {'image': IMAGE_PNG_ENCODED_STRING, 'name': 'image1.png'}
        request = dummy_request(self.dbsession, method='POST')
        request.json_body = params
        response = image_list(request)

        assert response.code == 201
        query = self.dbsession.query(Image)
        assert query.count() == 1

    def test_register_image_jpg(self):
        params = {'image': IMAGE_JPG_ENCODED_STRING, 'name': 'image1.jpg'}
        request = dummy_request(self.dbsession, method='POST')
        request.json_body = params
        response = image_list(request)

        assert response.code == 201
        query = self.dbsession.query(Image)
        assert query.count() == 1

    def test_get_single_image(self):
        params = {'image': IMAGE_JPG_ENCODED_STRING}
        request = dummy_request(self.dbsession, method='POST')
        request.json_body = params
        response = image_list(request)
        image_id = response.content.get('id')

        request_retrive = dummy_request(self.dbsession, method='GET')
        request_retrive.matchdict = {'id': image_id}
        response = image_detail(request_retrive)

        assert response.code == 200

    def test_get_image_list(self):
        dbsession = self.dbsession
        request = dummy_request(dbsession)

        params = {'image': IMAGE_JPG_ENCODED_STRING}
        request = dummy_request(dbsession, json_body=params, method='POST')
        response1 = image_list(request)

        params2 = {'image': IMAGE_PNG_ENCODED_STRING}
        request2 = dummy_request(dbsession, json_body=params2, method='POST')
        response2 = image_list(request2)

        request_get = dummy_request(dbsession, json_body=params2, method='GET')

        response_get = image_list(request_get)

        assert response_get.code == 200
        json_body = response_get.content

        assert len(json_body) == 2
        id_list = [obj.get('id') for obj in json_body]

        assert response1.content.get('id') in id_list
        assert response2.content.get('id') in id_list

    def test_update_image_png_to_jpg(self):
        dbsession = self.dbsession
        params = {'image': IMAGE_PNG_ENCODED_STRING}
        request_png = dummy_request(dbsession, json_body=params, method='POST')
        response_png = image_list(request_png)
        image_id = response_png.content.get('id')

        assert response_png.code == 201
        query = dbsession.query(Image)
        assert query.count() == 1

        image_png = query.first()
        assert image_png.id == image_id
        assert image_png.format == 'png'

        params_jpg = {'image': IMAGE_JPG_ENCODED_STRING}
        request = dummy_request(dbsession, json_body=params_jpg, method='PUT')
        request.matchdict = {'id': image_id}
        response_jpg = image_detail(request)

        assert response_jpg.code == 200
        assert query.count() == 1

        assert image_png.id == image_id
        assert image_png.format == 'jpeg'

    def test_delete_instance(self):
        dbsession = self.dbsession
        params = {'image': IMAGE_PNG_ENCODED_STRING}
        request = dummy_request(dbsession, json_body=params, method='POST')
        response = image_list(request)
        image_id = response.content.get('id')

        assert response.code == 201
        query = self.dbsession.query(Image)
        assert query.count() == 1

        image_png = query.first()
        assert image_png.id == image_id
        assert image_png.format == 'png'

        request = dummy_request(dbsession, method='DELETE')
        request.matchdict = {'id': image_id}
        response = image_detail(request)

        assert response.code == 200
        assert query.count() == 0
