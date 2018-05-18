import base64
import os
import transaction
import unittest

from pyramid import testing

from image_api.core.models import ModelBase
from image_api.core.models import get_engine
from image_api.core.models import get_session_factory
from image_api.core.models import get_tm_session


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
        ModelBase.metadata.create_all(self.engine)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()
        ModelBase.metadata.drop_all(self.engine)
