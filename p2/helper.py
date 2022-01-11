import traceback
import requests


UA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"


def req(method: str, url: str, **kwargs):
    kwargs.setdefault("headers", dict())
    kwargs['headers'].setdefault('User-Agent', UA)

    try:
        return requests.request(method.upper(), url, **kwargs)
    except requests.exceptions.InvalidURL:
        return False

    except (ConnectionError, requests.exceptions.RequestException):
        print("Unable connect to ", url)
        print(traceback.format_exc())  # Log full error message(full stack trace)

        return None


def is_dk_product_url(maybe_url):
    if not isinstance(maybe_url, str):
        return False

    return 'digikala.com/product/dkp-' in maybe_url
