from core import crawl, parse
from tg import get_updates, send_help, tg_formatter, send_msg
from helper import is_dk_product_url
import time
import traceback


def process():
    for update in get_updates():

        chat_id = update['message']['chat']['id']
        txt = update['message']['text']

        if txt == "/start":
            send_help(chat_id)
            continue

        if not is_dk_product_url(txt):
            send_help(chat_id, update['message']['message_id'])
            continue

        content = crawl(txt)
        if content is None:
            send_help(chat_id, update['message']['message_id'])
            continue

        send_msg(chat_id, tg_formatter(parse(content)), update['message']['message_id'])


def main():
    running = True

    while True:
        try:
            process()
        except KeyboardInterrupt:
            running = False
            break

        except Exception:
            print(traceback.format_exc())

        finally:
            if running:
                try:
                    time.sleep(10)
                except KeyboardInterrupt:
                    break


if __name__ == "__main__":
    main()
