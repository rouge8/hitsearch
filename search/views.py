from search import app
from search.database import db_session

@app.route('/')
def index():
    return 'Hello World!'

