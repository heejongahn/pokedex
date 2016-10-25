import random

from flask import render_template, request, redirect, flash, session, jsonify

from pokedex import app, db
from pokedex.models import LocaleType, GenderType, Pokemon, PokemonLocale
from pokedex.crawl import construct_name_map, crawl_pokemon

def init_view(app):
    # Construct name map
    name_map = construct_name_map()

    @app.route('/')
    def index():
        return render_template('index.html',
                random_pokemon=random.choice(name_map[LocaleType.EN]))

    @app.route('/<name_or_id>')
    def pokename(name_or_id):
        locale_name_map = name_map[LocaleType.EN]
        (poke_id, name) = parse_name(name_or_id, locale_name_map)
        if poke_id is None:
            return render_template('no_such_pokemon.html')

        info = crawl_pokemon(LocaleType.EN, name)
        (image_url, gender, poke_type, height, weight) = info[0]
        (description, category) = info[1]
        chain_ids = info[2]

        # chain_ids = ['1', '2,3,4']
        #             -> ['1', ['2', '3', '4']]
        #             -> [('1', 'name1'), [('2', 'name2'), ...]]
        chain_ids_splitted = [ids.split(',') for ids in chain_ids]
        chain_pairs = [
                [(poke_id, locale_name_map[int(poke_id)-1])
                    for poke_id in poke_ids]
                for poke_ids in chain_ids_splitted]

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

        return render_template('pokemon.html', p=p, p_locale=p_locale,
                chain_pairs=chain_pairs)

    @app.route('/name_map')
    def get_name_map():
        locale_name_map = name_map[LocaleType.EN]
        return jsonify(name_map=locale_name_map)

def parse_name(name_or_id, locale_name_map):
    try:
        poke_id = int(name_or_id)
        name = locale_name_map[poke_id-1]

    except:
        name = name_or_id.lower().capitalize()

    if name not in locale_name_map:
        return (None, None)

    poke_id = locale_name_map.index(name) + 1
    return (poke_id, name)
