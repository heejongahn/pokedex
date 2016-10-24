from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Warmest welcome from pokedex."

if __name__ == '__main__':
    app.run()
