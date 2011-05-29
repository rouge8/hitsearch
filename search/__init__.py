from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hitsearch.db'
db = SQLAlchemy(app)

import search.views
import search.models
# import search.database
