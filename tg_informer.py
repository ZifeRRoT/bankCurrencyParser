import os
import telegram


def send_error(func):
    token = os.environ.get("TG_INFORMER_TOKEN")
    chat_id = os.environ.get("TG_CHAT_ID")
    bot = telegram.Bot(token)

    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            bot.send_message(text=f"{func.__module__}: {e}", chat_id=chat_id)
    return inner
