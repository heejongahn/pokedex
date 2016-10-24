from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import crawl

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

name_map = None

@app.route('/')
def index():
    return "Warmest welcome from pokedex."

if __name__ == '__main__':
    name_map = crawl.construct_name_map()
    app.run()
