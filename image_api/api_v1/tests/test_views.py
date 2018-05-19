import base64
import json
import os
import transaction
import unittest

from pyramid import testing

from image_api.core.models import Base
from image_api.core.models import get_engine
from image_api.core.models import get_session_factory
from image_api.core.models import get_tm_session

from image_api.api_v1.models import Image
from image_api.api_v1.views import image_detail
from image_api.api_v1.views import image_list

from .settings import DIR_PATH
from .settings import IMAGE_JPG
from .settings import IMAGE_JPG_ENCODED
from .settings import IMAGE_JPG_ENCODED_STRING
from .settings import IMAGE_PNG
from .settings import IMAGE_PNG_ENCODED
from .settings import IMAGE_PNG_ENCODED_STRING


def dummy_request(dbsession=None, **kwargs):
    return testing.DummyRequest(dbsession=dbsession, **kwargs)


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('image_api.core')
        settings = self.config.get_settings()

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.dbsession = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class ImageRestApiTests(BaseTest):

    def setUp(self):
        super(ImageRestApiTests, self).setUp()
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

    def test_get_image_metadata(self):
        params = {'image': IMAGE_JPG_ENCODED_STRING, 'name': 'image1.jpg'}
        request = dummy_request(self.dbsession, method='GET')
        request.json_body = params
        response = image_list(request)

        request_retrive = dummy_request(self.dbsession)
        request_retrive.matchdict = {'id': ''}
        response = image_detail(request_retrive)

        assert response

    def test_get_image_list(self):
        request = dummy_request(self.dbsession)
        # request.matchdict = {'file': img}
        response = image_detail(request)

        # assert response
        # print(response)

    # def test_update_image(self):
    #     request = dummy_request(self.dbsession)
    #     img = open('resources/pyramid-logo.jpg', 'r')
    #     request.matchdict = {'file': img}
    #     response = image_detail(request)

    #     # assert response
    #     print(response)


# class TestMyViewSuccessCondition(BaseTest):

#     def setUp(self):
#         super(TestMyViewSuccessCondition, self).setUp()
#         self.init_database()

#         model = Image(name='one', size=55)
#         self.dbsession.add(model)

#     def test_passing_view(self):
#         info = my_view(dummy_request(self.dbsession))
#         assert type(info) == dict
        # self.assertEqual(info['one'].name, 'one')
        # self.assertEqual(info['project'], 'image-api')


# class TestMyViewFailureCondition(BaseTest):

#     def test_failing_view(self):
#         info = my_view(dummy_request(self.dbsession))
#         self.assertEqual(info.status_int, 500)
