import base64
import os
import transaction
import unittest

from pyramid import testing

from image_api.core.models import Base
from image_api.core.models import get_engine
from image_api.core.models import get_session_factory
from image_api.core.models import get_tm_session


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        settings = self.config.get_settings()

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.dbsession = get_tm_session(session_factory, transaction.manager)

        self.config.add_request_method(
            # r.tm is the transaction manager used by pyramid_tm
            lambda r: get_tm_session(session_factory, r.tm),
            'dbsession',
            reify=True
        )

    def init_database(self):
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)
