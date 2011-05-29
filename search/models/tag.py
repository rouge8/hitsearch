from search import db

class Tag(db.Model):
    """Represents a tag containing some sort of information."""
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    importance = db.Column(db.Float)
    tag = db.Column(db.String)

    __table_args__ = (db.UniqueConstraint("page_id", "tag"), {})

    def __init__(self, tag, page_id, importance):
        self.page_id = page_id
        self.importance = importance
        self.tag = tag
