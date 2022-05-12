from telegram import *
from telegram.ext import *
import config
import brain

telegramBot = Updater(config.TELEGRAM_KEY)
dispatch = telegramBot.dispatcher

def telegram_getMsg(telegramBot, context):
    userMsg = str(telegramBot.message.text).strip(config.UNWANTED_CHARS).lower()
    telegram_request = brain.TelegramQuery(userMsg)
    response = str(telegram_request.action_Router()).replace('news-Data','').replace('translatedText','')
    try:
        telegramBot.message.reply_text(response)
    except:
        telegramBot.message.reply_text('Something went wrong! 😅')        

def botEngine():
    print('Monalisa.AI is online on Telegram')
    dispatch.add_handler(MessageHandler(Filters.text, telegram_getMsg))
    telegramBot.start_polling()
    #telegramBot.idle() throwing value error on seperate thread