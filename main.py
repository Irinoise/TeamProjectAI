import telebot
from telebot import types

# http://t.me/movies_revenue_prediction_bot

token = '5216695845:AAFwPhtMXamZYg-nF7HqPplgv4KhJvGeW6k'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def cmd_start(message):
    pass


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, 'Привет! Я помогу тебе разобраться в моей работе. У меня есть следующие команды: \n \n'
                                      '/dataset_info - получить информацию о наборе данных \n'
                                      '/models_info - получить описание моделей')


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

    
def cmd_models_info_link(message):
    if message.text == "Линейная регрессия":
        return 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html'
    elif message.text == "Случайный лес":
        return 'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html'
    elif message.text == "Многослойный перцептрон":
         return 'https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html'
    else:
        return "Выберите представленную в списке интересующую модель"

      
@bot.message_handler(content_types=["text"])
def cmd_models_info_reply(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 'Перейти по ссылке scikit-learn и узнать о модели ' + message.text.lower() +': '+
                     cmd_models_info_link(
                                                                                                  message), reply_markup=markup)

bot.infinity_polling()
