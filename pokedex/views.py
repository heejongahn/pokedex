from flask import render_template, request, redirect, flash, session

from pokedex import app, db
from pokedex.models import LocaleType, GenderType, Pokemon, PokemonLocale
from pokedex.crawl import construct_name_map, crawl_pokemon

def init_view(app):
    # Construct name map
    name_map, name_array_map = construct_name_map()

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

        if name not in name_array_map[LocaleType.EN]:
            return render_template('no_such_pokemon.html')

        info = crawl_pokemon(LocaleType.EN, name)
        (poke_id, image_url, gender, poke_type, height, weight) = info[0]
        (name, description, category) = info[1]

        p = Pokemon.query.get(poke_id)
        if p is None:
            p = Pokemon(poke_id, image_url, gender, poke_type, height, weight)
            db.session.add(p)
            db.session.commit()

        p_locale = PokemonLocale.query.get((poke_id, LocaleType.EN))
        if p_locale is None:
            p_locale = PokemonLocale(poke_id, LocaleType.EN, name, description,
                    category, p.poke_id)
            db.session.add(p_locale)
            db.session.commit()

        return render_template('pokemon.html', p=p, p_locale=p_locale)
