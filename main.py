import requests
import telebot
from telebot import types

# http://t.me/movies_revenue_prediction_bot

token = '5216695845:AAFwPhtMXamZYg-nF7HqPplgv4KhJvGeW6k'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def cmd_start(message):
    return
@bot.message_handler(commands=['help'])
def cmd_help(message):
    return
@bot.message_handler(commands=['dataset_info'])
def cmd_dataset_info(message):
    return

@bot.message_handler(commands=['models_info'])
def cmd_models_info(message):
    user_markup = types.ReplyKeyboardMarkup()
    lr_button = types.KeyboardButton("Линейная регрессия")
    rf_button = types.KeyboardButton("Случайный лес")
    mlp_button = types.KeyboardButton("Многослойный перцептрон")
    user_markup.row(lr_button, rf_button, mlp_button)
    bot.send_message(message.chat.id, "Выберите интересующую модель", reply_markup=user_markup)

bot.infinity_polling()