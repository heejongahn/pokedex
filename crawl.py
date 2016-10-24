from requests import get
from lxml import html

BASE_KR = 'http://ko.pokemon.wikia.com/wiki/{}'
BASE_EN = 'http://www.pokemon.com/us/pokedex/{}'
NAME_MAP = 'http://ko.pokemon.wikia.com/wiki/%EA%B5%AD%EA%B0%80%EB%B3%84_%ED%8F%AC%EC%BC%93%EB%AA%AC_%EC%9D%B4%EB%A6%84_%EB%AA%A9%EB%A1%9D'

def fetch_and_parse(url):
    r = get(url)
    doc = html.fromstring(r.content)

    return doc

def construct_name_map():
    name_map = {}
    doc = fetch_and_parse(NAME_MAP)

    table = doc.cssselect('div.WikiaArticle table.prettytable')[0]
    rows = table.findall('tr')[1:]

    for row in rows:
        tds = row.findall('td')
        poke_no = tds[0].text.strip()

        # KR name is enclosed in an additional <a> tag
        kr_name = tds[1].getchildren()[0].text.strip()
        jp_name = tds[2].text.strip()
        en_name = tds[3].text.strip()

        name_map[poke_no] = (kr_name, jp_name, en_name)

    return name_map
