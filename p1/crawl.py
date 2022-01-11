import requests

url = "https://www.digikala.com/product/dkp-6459793"
response = requests.get(url)

with open('product.html', 'w') as fh:
    fh.write(response.text)
