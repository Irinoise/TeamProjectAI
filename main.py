import telebot
import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# http://t.me/movies_revenue_prediction_bot

token = '5216695845:AAFwPhtMXamZYg-nF7HqPplgv4KhJvGeW6k'
bot = telebot.TeleBot(token)

durl='https://www.dropbox.com/s/m7z8uj88smjjhd4/movies_raw_dataset.csv?dl=0'
data = pd.read_csv('movies.csv', sep='\t')
#csv изменен, убраны заголовки и файл разобран по конкретным колонкам
data1 =pd.read_csv('movies1.csv', delimiter=',', names=['id','belongs_to_collection','budget','genres','homepage','imdb_id','original_language','original_title','overview','popularity','poster_path','production_companies','production_countries','release_date','runtime','spoken_languages','status','tagline','title','Keywords','cast','crew','revenue'])


@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id,
                     'Привет!')

@bot.message_handler(commands=['stop'])
def cmd_start(message):
    bot.send_message(message.chat.id,
                     'Пока!')


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id,
                     'Привет! Я помогу тебе разобраться в моей работе. У меня есть следующие команды: \n \n'
                     '/dataset_info - получить информацию о наборе данных \n'
                     '/models_info - получить описание моделей')


@bot.message_handler(commands=['dataset_info'])
def cmd_dataset_info(message):
    bot.send_message(message.chat.id, 'Dataset доступен по ссылке ' + durl + ' и состоит из полей:')
    bot.send_message(message.chat.id, str(data1.columns.tolist()))
    bot.send_message(message.chat.id, str(data1.describe()))

# @bot.message_handler(commands=['models_info'])
# def cmd_models_info(message):
#    pass

if __name__ == '__main__':
    bot.infinity_polling()