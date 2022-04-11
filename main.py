import telebot

# http://t.me/movies_revenue_prediction_bot

token = '5216695845:AAFwPhtMXamZYg-nF7HqPplgv4KhJvGeW6k'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def cmd_start(message):


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, 'Привет! Я помогу тебе разобраться в моей работе. У меня есть следующие команды: \n \n'
                                      '/dataset_info - получить информацию о наборе данных \n'
                                      '/models_info - получить описание моделей')


#@bot.message_handler(commands=['dataset_info'])
#def cmd_dataset_info(message):
#    pass



#@bot.message_handler(commands=['models_info'])
#def cmd_models_info(message):
#    pass

if __name__ == '__main__':
    bot.infinity_polling()