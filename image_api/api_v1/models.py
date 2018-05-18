import enum

from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import Enum

from image_api.core.models import ModelBase


class ImageFormatEnum(enum.Enum):
    JPEG = 'jpeg'
    PNG = 'png'


class Image(ModelBase):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(Integer)
    format = Column(Enum(ImageFormatEnum))
    width = Column(Integer)
    length = Column(Integer)
    filename = Column(String)

    def store_file(self):
        pass

    def retrive_file(self):
        pass

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self, serialize_fields=[]):
        if not serialize_fields:
            serialize_fields = [
                'id', 'name', 'size', 'format', 'width',
                'length', 'filename'
            ]

        d = {}
        for attr_name in serialize_fields:
            d[attr_name] = getattr(self, attr_name)
        return d


# class Note(ModelBase):
#     __tablename__ = 'Note'
#     id = Column(Integer, primary_key=True)
#     title = Column(Text)
#     description = Column(Text)
#     create_at = Column(Text)
#     create_by = Column(Text)
#     priority = Column(Integer)

#     def __init__(self, title, description, create_at, create_by, priority):
#         self.title = title
#         self.description = description
#         self.create_at = create_at
#         self.create_by = create_by
#         self.priority = priority

#     @classmethod
#     def from_json(cls, data):
#         return cls(**data)

#     def to_json(self):
#         to_serialize = ['id', 'title', 'description', 'create_at', 'create_by', 'priority']
#         d = {}
#         for attr_name in to_serialize:
#             d[attr_name] = getattr(self, attr_name)
#         return d


Index('image_index', Image.name, unique=True, mysql_length=255)
