from sqlalchemy import Column, Integer, String, DateTime, Float # and whatever other things we need
from hitsearch.database import Base
import datetime

class Page(Base):
    """Represents a webpage in the database."""
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    discovery_time = Column(DateTime)
    authority = Column(Float)
    hubbiness = Column(Float)

    def __init__(self, url):
        self.url = url
        self.discovery_time = datetime.datetime.now()
        self.authority = None
        self.hubbiness = None

