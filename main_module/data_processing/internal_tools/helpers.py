import telebot
from decouple import config


def send_message_tg(msg):
    api_key = config("TG_BOT_API_KEY")
    chat_id = config("TG_BOT_CHAT_ID")
    if not api_key:
        raise Exception("No env variable for telegram bot!")
    if not chat_id:
        raise Exception("No env variable for telegram chat id!")
    bot = telebot.TeleBot(api_key)
    bot.send_message(chat_id, msg)
