import telebot
from stocks import StockInfo
from currency import CurrencyInfo
from bs4 import BeautifulSoup  # Либа для красивого текста и чтения xml формата
import reticker  # Либа для проверки существует ли такой тикер (аля regex)
import yaml  # Либа для .yml
from yaml.loader import SafeLoader
import logging  # Для логов в терминале

with open('config.yml') as f:
    cfg = yaml.load(f, Loader=SafeLoader)

token = cfg['tg']['bot_token']
bot = telebot.TeleBot(token, parse_mode=None)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

help = BeautifulSoup(open("help.txt", "r"), "lxml")


# Вывести список команд
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, help.get_text(), parse_mode='HTML')


# Вывод информации об акции
@bot.message_handler(commands=['stock'])
def text_supergroup_stock(message):
    extractor = reticker.TickerExtractor()
    ticker = extractor.extract(message.text)
    if len(ticker) == 0:
        markup = telebot.types.ReplyKeyboardMarkup()
        sberkey = telebot.types.KeyboardButton('/stock SBER')
        gazpkey = telebot.types.KeyboardButton('/stock GAZP')
        tcsgkey = telebot.types.KeyboardButton('/stock TCSG')
        exitkey = telebot.types.KeyboardButton('/exit')
        markup.row(sberkey, gazpkey, tcsgkey)
        markup.row(exitkey)
        return bot.reply_to(message, "To get stock's information send me a ticker.\n\n<b>Example</b>: /stock SBER",
                            parse_mode='HTML', reply_markup=markup)
    elif 3 > len(ticker[0]) or len(ticker[0]) > 7:
        return bot.reply_to(message, "That's not a valid ticker! Try again.\n\n<b>Example</b>: "
                                     "/stock SBER", parse_mode='HTML')
    check = StockInfo(ticker[0])
    bot.reply_to(message, check.get_info(), parse_mode='HTML')


# Вывод информации о валюте
@bot.message_handler(commands=['currency'])
def text_supergroup_currency(message):
    ticker = message.text[10:].upper().strip('')
    if len(ticker) == 0:
        markup = telebot.types.ReplyKeyboardMarkup()
        usdkey = telebot.types.KeyboardButton('/currency USD')
        eurkey = telebot.types.KeyboardButton('/currency EUR')
        cnykey = telebot.types.KeyboardButton('/currency CNY')
        exitkey = telebot.types.KeyboardButton('/exit')
        markup.row(usdkey, eurkey, cnykey)
        markup.row(exitkey)
        return bot.reply_to(message, "To get currency's rate send me a ticker.\n\n<b>Example</b>: /currency EUR",
                            parse_mode='HTML', reply_markup=markup)
    elif 3 > len(ticker) or len(ticker) > 3:
        return bot.reply_to(message, "That's not a valid ticker! Try again.\n\n<b>Example</b>: "
                                     "/currency EUR", parse_mode='HTML')
    check = CurrencyInfo(ticker)
    bot.reply_to(message, check.get_info(), parse_mode='HTML')


# Выход
@bot.message_handler(commands=['exit'])
def text_supergroup_currency(message):
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, "Done!", reply_markup=markup)


bot.infinity_polling()
