import transaction

from image_api.api_v1.models import Image
from image_api.api_v1.tests import BaseTest
from image_api.api_v1.utils import extract_metadata

from .settings import IMAGE_JPG


class ImageModelTests(BaseTest):

    def setUp(self):
        super(ImageModelTests, self).setUp()
        self.init_database()

    def test_create_instance(self):
        metadata = extract_metadata(IMAGE_JPG)
        image = Image()
        image.size = metadata.get('size')
        self.dbsession.add(image)
        self.dbsession.flush()
        query = self.dbsession.query(Image)

        assert query.count() == 1
        # assert
