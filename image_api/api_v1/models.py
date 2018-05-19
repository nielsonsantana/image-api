import enum

from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import Enum

from image_api.core.models import Base
from .utils import extract_metadata


class ImageFormatEnum(enum.Enum):
    JPEG = 'jpeg'
    PNG = 'png'


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(Integer)
    format = Column(String)
    width = Column(Integer)
    length = Column(Integer)
    filename = Column(String)
    extension = Column(String)

    image = None

    def save(self, dbsession):
        dbsession.add(self)
        dbsession.flush()

    def retrive_file(self):
        pass

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def __json__(self):
        return self.to_json()

    def to_json(self, serialize_fields=[]):
        if not serialize_fields:
            serialize_fields = [
                'id', 'name', 'size', 'format', 'width',
                'length', 'filename'
            ]

        d = {}
        for attr_name in serialize_fields:
            d[attr_name] = getattr(self, attr_name)

        d.update(url=self.get_absolute_url_image())
        return d

    def get_absolute_url_image(self):
        pass

    image_url = property(get_absolute_url_image)

    def update(self, **kwargs):
        update_fields = [
            'name', 'size', 'format', 'width', 'length', 'filename',
            'extension'
        ]
        for attr_name, value in kwargs.items():
            if attr_name in update_fields:
                setattr(self, attr_name, value)

    def update_image_matadata(self, image_path):
        """
        Arg:
            image_path - Receives a image path
        """
        metadata = extract_metadata(image_path)
        self.update(**metadata)


Index('image_index', Image.name, unique=False, mysql_length=255)
