from flask import render_template, request, redirect, flash, session

from pokedex import app
from pokedex.models import LocaleType, GenderType, Pokemon, PokemonLocale
from pokedex.crawl import construct_name_map, crawl_pokemon

def init_view(app):
    # Construct name map
    name_map = construct_name_map()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/<name_or_id>')
    def pokename(name_or_id):
        try:
            poke_id = int(name_or_id)

            # English name default
            name = name_map[poke_id][2]

        except:
            name = name_or_id

        if name not in construct_name_map().values():
            return "No such pokemon :("

        return crawl_pokemon(LocaleType.EN, name)
