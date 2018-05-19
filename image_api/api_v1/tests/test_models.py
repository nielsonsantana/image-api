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
        image.format = metadata.get('format')
        image.width = metadata.get('width')
        image.length = metadata.get('length')
        image.extension = metadata.get('extension')

        query = self.dbsession.query(Image)

        self.dbsession.add(image)
        transaction.commit()
        query = self.dbsession.query(Image)

        assert query.count() == 1

        obj = self.dbsession.query(Image).first()
        assert obj.size == metadata.get('size')
        assert obj.format == metadata.get('format')
        assert obj.width == metadata.get('width')
        assert obj.length == metadata.get('length')
        assert obj.extension == metadata.get('extension')

    def test_update_instance(self):
        image = Image()
        metadata = extract_metadata(IMAGE_JPG)
        image.update(**metadata)

        assert image.size == metadata.get('size')
        assert image.format == metadata.get('format')
        assert image.width == metadata.get('width')
        assert image.length == metadata.get('length')
        assert image.extension == metadata.get('extension')

    def test_delete_instance(self):
        image = Image()
        metadata = extract_metadata(IMAGE_JPG)
        image.update(**metadata)
        image.save(self.dbsession)

        query = self.dbsession.query(Image)
        assert query.count() == 1
        query.filter_by(id=image.id).delete()

        assert query.count() == 0
