from core import crawl, parse
from tg import send_help, tg_formatter, send_msg
from helper import is_dk_product_url
from flask import Flask, request

base_url = ""
wh_token = "eQx6408uyyBReuHe"

app = Flask(__name__)


def process(update):
    chat_id = update['message']['chat']['id']
    txt = update['message']['text']

    if txt == "/start":
        send_help(chat_id)
        return

    if not is_dk_product_url(txt):
        send_help(chat_id, update['message']['message_id'])
        return

    content = crawl(txt)
    if content is None:
        send_help(chat_id, update['message']['message_id'])
        return

    send_msg(chat_id, tg_formatter(parse(content)), update['message']['message_id'])


@app.post("/wh")
def web_hook_callback():
    try:
        data = request.json
    except Exception:
        return ""

    if wh_token not in request.query_string:
        return ""

    if not isinstance(data, dict) or "message" not in data or "text" not in data['message']:
        return ""

    process(data)


def main():
    app.run('0.0.0.0', 4646)


if __name__ == "__main__":
    main()
