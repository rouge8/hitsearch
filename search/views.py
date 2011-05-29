from search import app
from search.database import db_session

@app.route('/')
def index():
    return 'Hello World!'

@app.after_request
def shutdown_session(response):
    db_session.remove()
    return response
