import transaction
import unittest

from pyramid import testing

from image_api.core.models import get_engine
from image_api.core.models import get_session_factory
from image_api.core.models import get_tm_session
from image_api.core.models import ModelBase
from image_api.core.views import my_view

from image_api.api_v1.models import Image


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('image_api.core')
        settings = self.config.get_settings()

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        ModelBase.metadata.create_all(self.engine)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()
        ModelBase.metadata.drop_all(self.engine)


class TestMyViewSuccessCondition(BaseTest):

    def setUp(self):
        super(TestMyViewSuccessCondition, self).setUp()
        self.init_database()

        model = Image(name='one', value=55)
        self.session.add(model)

    def test_passing_view(self):
        info = my_view(dummy_request(self.session))
        assert type(info) == dict
        # self.assertEqual(info['one'].name, 'one')
        # self.assertEqual(info['project'], 'image-api')


# class TestMyViewFailureCondition(BaseTest):

#     def test_failing_view(self):
#         info = my_view(dummy_request(self.session))
#         self.assertEqual(info.status_int, 500)
