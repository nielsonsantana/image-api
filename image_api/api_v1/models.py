import enum

from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import Enum

from image_api.core.models import Base


class ImageFormatEnum(enum.Enum):
    JPEG = 'jpeg'
    PNG = 'png'


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(Integer)
    format = Column(Enum(ImageFormatEnum))
    width = Column(Integer)
    length = Column(Integer)
    filename = Column(String)

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


Index('image_index', Image.name, unique=False, mysql_length=255)
