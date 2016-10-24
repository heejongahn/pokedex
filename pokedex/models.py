import enum
from pokedex import db

# Enum Definitions

class LocaleType(enum.Enum):
    KR = "kr"
    JP = "jp"
    EN = "en"


class GenderType(enum.Enum):
    UNKNOWN = "?"
    ONLY_MALE = "♂"
    ONLY_FEMALE = "♀"
    BOTH_GENDER = "♀ ♂"


# Actual Models

class Pokemon(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(120))
    gender = db.Column(db.Enum(GenderType))
    poke_type = db.Column(db.String(20))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    locales = db.relationship('PokemonLocale', backref='basics')

    def __init__(self, p_id, i, g, p_type, h, w):
        self.poke_id = p_id
        self.image_url = i
        self.gender = g
        self.poke_type = p_type
        self.height = h
        self.weight = w


class PokemonLocale(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    locale = db.Column(db.Enum(LocaleType), primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    category = db.Column(db.String(20))
    basics_id = db.Column(db.Integer, db.ForeignKey('pokemon.poke_id'))

    def __init__(self, p_id, l, n, d, c, b_id):
        self.poke_id = p_id
        self.locale = l
        self.name = n
        self.description = d
        self.category = c
        self.basics_id = b_id
