from flask import render_template, request, redirect, flash, session

from pokedex import app
from pokedex.models import LocaleType, GenderType, Pokemon, PokemonLocale

@app.route('/')
def index():
    return "Warmest welcome from pokedex."
