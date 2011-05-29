from search import db

class Link(db.Model):
    """Represents a link between two pages."""
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.String, db.ForeignKey('pages.id'))
    source_id = db.Column(db.String, db.ForeignKey('pages.id'))
    target = db.relationship('Page', backref=db.backref('pages', lazy='dynamic'))
    source = db.relationship('Page', backref=db.backref('pages', lazy='dynamic'))

    text = db.Column(db.String)
    __table_args__ = (db.UniqueConstraint("target_id", "source_id", "text"), {})

    def __init__(self, target, source, text):
        self.target_id = target_id
        self.source_id = source_id
        self.text = text
