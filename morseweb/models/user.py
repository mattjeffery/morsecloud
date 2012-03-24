from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
    )

from morseweb.models import Base

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(25), unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value
