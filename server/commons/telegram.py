import telegram
import os

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

autoBot = telegram.Bot(token=TELEGRAM_TOKEN)
autoBot.send_message(chat_id=TELEGRAM_CHAT_ID, text='TEST')