import requests
from bs4 import BeautifulSoup


session = requests.Session()


def crawl(url):
    r = session.get(url)

    if r.status_code != 200:
        return None

    return r.text


def parse(content):
    soup = BeautifulSoup(content, 'html.parser')

    title = " ".join(soup.find('h1', {'class': 'c-product__title'}).text.split()).strip()
    price = " ".join(soup.find('div', {'class': 'c-product__seller-price-pure js-price-value'}).text.split()).strip()

    # ul(1) -> li(n) -> div(2) -> text

    ul = soup.find('ul', {'class': 'c-params__list'})
    specifications: dict[str, list] = {}
    last_key = ""

    for li in ul.find_all('li'):
        # info = li.find_all('div', recursive=False)
        # key = info[0]
        # value = info[1]

        key = li.find('div', {'class': 'c-params__list-key'})
        value = li.find('div', {'class': 'c-params__list-value'})

        key = " ".join(key.text.split()).strip()
        value = " ".join(value.text.split()).strip()

        if key == "":
            specifications[last_key].append(value)
            continue

        last_key = key
        if key not in specifications:
            specifications[key] = []

        specifications[key].append(value)

    return dict(title=title, price=price, specifications=specifications)
