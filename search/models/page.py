from search import db
import datetime

class Page(db.Model):
    """Represents a webpage in the database."""
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True)
    discovery_time = db.Column(db.DateTime)
    authority = db.Column(db.Float)
    hubbiness = db.Column(db.Float)

    tags = db.relationship('Tag', backref='pages', lazy='dynamic')

    def __init__(self, url):
        self.url = url
        self.discovery_time = datetime.datetime.now()
        self.authority = None
        self.hubbiness = None

