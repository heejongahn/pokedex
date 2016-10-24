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
    name_map = {}
    doc = fetch_and_parse(NAME_MAP_URL)

    table = doc.cssselect('div.WikiaArticle table.prettytable')[0]
    rows = table.findall('tr')[1:]

    name_array_map = {
            LocaleType.KR: [],
            LocaleType.EN: [],
            LocaleType.JP: []
            }

    for row in rows:
        tds = row.findall('td')
        poke_no = tds[0].text.strip()

        # KR name is enclosed in an additional <a> tag
        kr_name = tds[1].getchildren()[0].text.strip()
        jp_name = tds[2].text.strip()
        en_name = tds[3].text.strip().lower()

        name_map[poke_no] = (kr_name, jp_name, en_name)
        name_array_map[LocaleType.KR].append(kr_name)
        name_array_map[LocaleType.JP].append(jp_name)
        name_array_map[LocaleType.EN].append(en_name)

    return (name_map, name_array_map)

def crawl_pokemon(locale, name):
    doc = fetch_and_parse(BASE_URLS[locale].format(name))

    if locale == LocaleType.KR:
        return parse_pokemon_kr(doc, name)
    else:
        return parse_pokemon_en(doc, name)

def parse_pokemon_en(doc, name):
    poke_id = doc.cssselect('span#pokemonID')[0].text[1:]

    image = doc.cssselect('div.profile-images')[0].getchildren()[0]
    image_url = image.get('src')[2:]

    # This contains height, weight, gender, category info
    ability_info = doc.cssselect('div.pokemon-ability-info')[0]
    [ height_span, weight_span, gender_span, category_span] = \
            ability_info.cssselect('li span.attribute-value')[:4]

    height, weight = resolve_american_units(height_span, weight_span)
    gender = figure_gender(gender_span)
    category = category_span.text

    poke_type = doc.cssselect('div.dtm-type a')[0].text

    description = doc.cssselect('div.version-descriptions')[0].\
            getchildren()[0].text.strip()

    return [poke_id, image_url, gender, poke_type, height, weight,
            LocaleType.EN, name, description, category]


# ------------------------------------------
# Below are helper functions used in crawler
# ------------------------------------------

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
