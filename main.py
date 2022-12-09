import telebot
from stocks import StockInfo
from currency import CurrencyInfo
from bs4 import BeautifulSoup
import reticker
token = "enter your token here."
bot = telebot.TeleBot(token, parse_mode=None)


help = BeautifulSoup(open("help.txt", "r"), "lxml")
# list of commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, help.get_text(), parse_mode='HTML')


# get stock info
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

@bot.message_handler(commands=['exit'])
def text_supergroup_currency(message):
	markup = telebot.types.ReplyKeyboardRemove(selective=False)
	bot.reply_to(message, "Done!", reply_markup=markup)

bot.infinity_polling()
