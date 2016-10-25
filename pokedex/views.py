import random

from flask import render_template, request, redirect, jsonify

from pokedex import app, db
from pokedex.models import LocaleType, Pokemon, PokemonLocale, Evolution
from pokedex.crawl import construct_name_map, crawl_pokemon

def init_view(app):
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

        p = Pokemon.query.get(poke_id)

        if p is None:
            info = crawl_pokemon(LocaleType.EN, name)
            (image_url, gender, poke_type, height, weight) = info[0]
            (description, category) = info[1]
            chain_ids = info[2]

            p = Pokemon(poke_id, image_url, gender, poke_type, height, weight)
            db.session.add(p)
            db.session.commit()

            chain_ids_splitted = [ids.split(',') for ids in chain_ids]
            make_evolution_records(chain_ids_splitted)

        else:
            chain_ids_splitted = get_evolution_records(poke_id)

        # chain_ids             : ['1', '2,3,4']
        # chain_ids_splitted    : ['2', ['3', '4']]
        # chain_pairs           : [('1', 'name1'), [('2', 'name2'), ...]]
        chain_pairs = [
                [(p_id, locale_name_map[int(p_id)-1]) for p_id in p_ids]
                for p_ids in chain_ids_splitted]

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

def make_evolution_records(chain_ids_splitted):
    chain_length = len(chain_ids_splitted)

    for i in range(chain_length-1):
        prv = chain_ids_splitted[i][0]
        nxts = chain_ids_splitted[i+1]

        for nxt in nxts:
            evolution = Evolution(int(prv), int(nxt))
            db.session.add(evolution)
            db.session.commit()

def get_evolution_records(poke_id):
    chain_ids_splitted = [[poke_id]]

    # Construct the previous part of the chain
    # Note that this is a one-way road.
    prv_pokemon = Evolution.query.filter_by(nxt=poke_id).first()
    while (prv_pokemon is not None):
        chain_ids_splitted.insert(0, [prv_pokemon.prv])
        prv_pokemon = Evolution.query.filter_by(nxt=prv_pokemon.prv).first()

    # Construct the remaining part of the chain
    nxt_pokemons = Evolution.query.filter_by(prv=poke_id).all()
    while (len(nxt_pokemons) > 0):
        # Multiple evolution (ex Eevee)
        if (len(nxt_pokemons) > 1):
            chain_ids_splitted.append([n.nxt for n in nxt_pokemons])
            break # Evolution chain ends when the chain diverges

        nxt_pokemon = nxt_pokemons[0]
        chain_ids_splitted.insert(0, [nxt_pokemon.nxt])
        nxt_pokemons = Evolution.query.filter_by(prv=nxt_pokemon.nxt).all()

    return chain_ids_splitted
