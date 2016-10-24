from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

name_map = None

from pokedex import models, crawl
from pokedex.views import init_view; init_view(app);
