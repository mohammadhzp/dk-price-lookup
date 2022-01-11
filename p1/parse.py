from bs4 import BeautifulSoup

with open('product.html') as fh:
    soup = BeautifulSoup(fh.read(), 'html.parser')

# soup.find() -> soup.find_all()
# soup.select_one() -> soup.select()

title = soup.find('h1', {'class': 'c-product__title'})
print(title.text.strip())

price = soup.find('div', {'class': 'c-product__seller-price-pure js-price-value'})
print(price.text.strip())


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

import json
print(json.dumps(specifications, ensure_ascii=False))

