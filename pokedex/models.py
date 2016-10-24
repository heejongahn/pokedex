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


class PokemonLocale(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    locale = db.Column(db.Enum(LocaleType), primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    category = db.Column(db.String(20))
