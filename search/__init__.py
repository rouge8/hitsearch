from flask import Flask
app = Flask(__name__)

import search.views
import search.models
import search.database
