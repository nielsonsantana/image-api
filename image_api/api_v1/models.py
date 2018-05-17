from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Text

from image_api.core.models import ModelBase


class Image(ModelBase):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


Index('image_index', Image.name, unique=True, mysql_length=255)
