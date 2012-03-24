from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
    DateTime,
    )

from morseweb.models import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True) # external soundcloud id
    name = Column(Unicode(128))
    shortname = Column(Unicode(128))
    access_token = Column(Unicode(128))
    expires_at = Column(DateTime, nullable=True, default=None)
    scope = Column(Unicode(128), nullable=True, default=None)
    refresh_token = Column(Unicode(128), nullable=True, default=None)
