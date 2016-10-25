from requests import get
from lxml import html

from pokedex.models import LocaleType, GenderType

BASE_URLS = {
        LocaleType.KR: 'http://ko.pokemon.wikia.com/wiki/{}',
        LocaleType.EN: 'http://www.pokemon.com/us/pokedex/{}'
        }

NAME_MAP_URL = 'http://ko.pokemon.wikia.com/wiki/%EA%B5%AD%EA%B0%80%EB%B3%84_%ED%8F%AC%EC%BC%93%EB%AA%AC_%EC%9D%B4%EB%A6%84_%EB%AA%A9%EB%A1%9D'

def fetch_and_parse(url):
    r = get(url)
    doc = html.fromstring(r.content)

    return doc

def construct_name_map():
    doc = fetch_and_parse(NAME_MAP_URL)

    table = doc.cssselect('div.WikiaArticle table.prettytable')[0]
    rows = table.findall('tr')[1:]

    name_map = {
            LocaleType.EN: []

            # Uncomment below when adding other locales

            # LocaleType.KR: [],
            # LocaleType.JP: []
            }

    for row in rows:
        tds = row.findall('td')
        poke_no = int(tds[0].text.strip())

        en_name = tds[3].text.strip().lower().capitalize()
        name_map[LocaleType.EN].append(en_name)

        # Uncomment below when adding other locales

        # KR name is enclosed in an additional <a> tag
        # kr_name = tds[1].getchildren()[0].text.strip()
        # jp_name = tds[2].text.strip()

        # name_map[LocaleType.KR].append(kr_name)
        # name_map[LocaleType.JP].append(jp_name)

    return name_map

def crawl_pokemon(locale, name):
    doc = fetch_and_parse(BASE_URLS[locale].format(sanitize(name)))

    if locale == LocaleType.KR:
        return parse_pokemon_kr(doc, name)
    else:
        return parse_pokemon_en(doc, name)

def parse_pokemon_en(doc, name):
    poke_id = strip_span(doc.cssselect('span#pokemonID')[0])

    image = doc.cssselect('div.profile-images')[0].getchildren()[0]
    image_url = 'https://' + image.get('src')[2:]

    # This contains height, weight, gender, category info
    ability_info = doc.cssselect('div.pokemon-ability-info')[0]
    [ height_span, weight_span, gender_span, category_span] = \
            ability_info.cssselect('li span.attribute-value')[:4]

    height, weight = resolve_american_units(height_span, weight_span)
    gender = figure_gender(gender_span)
    category = category_span.text

    poke_type_list = [a.text for a in doc.cssselect('div.dtm-type a')]
    # Make sure the list is unique
    poke_type = " ".join(list(set(poke_type_list)))

    description = doc.cssselect('div.version-descriptions')[0].\
            getchildren()[0].text.strip()

    return [
            (poke_id, image_url, gender, poke_type, height, weight),
            (name, description, category),
            get_evolution_chain(doc.cssselect('.pokedex-pokemon-evolution')[0])
            ]


def parse_pokemon_kr(doc, name):
    return 'Currently not implemented.'

# ------------------------------------------
# Below are helper functions used in crawler
# ------------------------------------------

# Thanks to Farfetch’d
def sanitize(name):
    return name.replace('’', '')

# Deals with the messed up American Unit System
def resolve_american_units(height_span, weight_span):
    [height_ft, height_inch] = \
            [float(h[:-1]) for h in height_span.text.split()]

    height = (height_ft * 12 + height_inch) * 0.0254
    weight = float(weight_span.text.split()[0]) * 0.453592

    # Ex:
    # 0.30479999999999996 m -> 0.3 m
    # 3.9916096000000003 kg -> 4.0 kg
    return (round(height, 2), round(weight, 2))

# Figure out which gender type a pokemon has
def figure_gender(gender_span):
    if gender_span.text.strip() == 'Unknown':
        gender = GenderType.UNKNOWN
    elif len(gender_span.getchildren()) == 2:
        gender = GenderType.BOTH_GENDER
    elif gender_span.findall('i.icon_female_symbol'):
        gender = GenderType.FEMALE
    else:
        gender = GenderType.MALE

    return gender

# Get evolution chain of a given pokemon.
# Returns list representing the poke_ids of evolution chain.
# Ex:
# ['001', '002', '003'] (Bulbasaur -> Ivysaur -> Venusaur)
# ['133', '134, 135, 136, 196, 197, 470, 471, 700'] (Eevee)
# ['83'] (Farfetch'd)
def get_evolution_chain(evo):
    pokemons = evo.cssselect('ul.evolution-profile > li')
    chain = []

    # No evolution info
    if len(pokemons) == 1:
        chain = [strip_span(pokemons[0].cssselect('span.pokemon-number')[0])]

    # Two step evolution
    elif len(pokemons) == 2:
        [first, last] = [p.cssselect('span.pokemon-number') for p in pokemons]

        # Evolves to multiple pokemon
        if len(last) > 1:
            evolved_from = strip_span(first[0])
            evolves_to = ",".join([strip_span(s) for s in last])
            chain = [evolved_from, evolves_to]

        # Regular two step evolution
        else:
            chain = [strip_span(s) for s in [first[0], last[0]]]

    else:
        # Three step evolution
        span_chain = [p.cssselect('span.pokemon-number')[0] for p in pokemons]
        chain = [strip_span(s) for s in span_chain]

    return chain

def strip_span(span):
    return span.text.strip(' \n#')
