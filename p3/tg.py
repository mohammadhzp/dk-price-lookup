from pathlib import Path
from typing import Optional
from helper import req
import traceback


BOT_TOKEN = "5070356113:AAExLjvs4Erewpa-eH6Zy1j515p3LTqg6b8"


UPDATE_LOCK = Path(__file__).parent / ".last_update_id"
UPDATE_LOCK.touch(exist_ok=True)


def save_update_id(update_id):
    UPDATE_LOCK.write_text(str(update_id))


def get_update_id() -> Optional[int]:
    try:
        return int(UPDATE_LOCK.read_text().strip())
    except (ValueError, TypeError):
        return None


def tg_formatter(data):
    output = f"<b>عنوان</b>: {data['title']}\n\n<b>قیمت</b>: {data['price']}T\n\n\n"

    if not data['specifications']:
        output += "این محصول دارای مشخصات نمی باشد\n"
        return output

    output += "<b>مشخصات</b>:\n"
    i = 1
    for k, v in data['specifications'].items():
        output += f"{i}- <b>{k}</b>: {v if isinstance(v, str) else ','.join(v)}\n"
        i += 1

    output += "\n‌"
    return output


def telegram_req(endpoint, data=None) -> Optional[dict]:
    r = req('POST', f"https://api.telegram.org/bot{BOT_TOKEN}/{endpoint}", json=data)
    if not r:
        return r

    try:
        data = r.json()

        # Refer to https://core.telegram.org/bots/api#making-requests
        if data['ok'] is False:
            print("Telegram call to", endpoint, "did not succeed")

            if "description" in data:
                print("Error description: ", data['description'])

            return None

        return data['result']

    except ValueError:
        print("Invalid json got from TG for ", endpoint, "endpoint")
        print("Response body", r.text, end="\n\n")
        print("Request body: ", data, end="\n\n")
        print(traceback.format_exc())


def get_updates():
    update_id = get_update_id()
    _data = None if update_id is None else dict(offset=update_id + 1)
    updates = telegram_req("getUpdates", _data)

    if not updates:
        return []

    for update in updates:
        save_update_id(update['update_id'])
        if "message" not in update:
            continue  # We got an update which does not include any message, no need to check it

        if "text" not in update['message']:
            continue

        yield update


def send_msg(chat_id, txt, reply_msg_id=None, **kwargs):
    kwargs.setdefault('parse_mode', 'HTML')

    return telegram_req("sendMessage", dict(
            chat_id=chat_id,
            text=txt,
            reply_to_message_id=reply_msg_id,
            **kwargs
        ))


def send_help(chat_id, reply_msg_id=None):
    return send_msg(chat_id, "شما باید لینک یک محصول در دیجی کالا را ارسال نمایید", reply_msg_id)
