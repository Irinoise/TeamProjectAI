import telebot
from telebot import types

# http://t.me/movies_revenue_prediction_bot

token = '5216695845:AAFwPhtMXamZYg-nF7HqPplgv4KhJvGeW6k'
bot = telebot.TeleBot(token)
models_dict = {
    'Линейная регрессия': 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression'
                          '.html',
    'Случайный лес': 'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html',
    'Многослойный перцептрон': 'https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor'
                               '.html'
}


@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я - бот, предсказывающий доход '
                                      f'фильма по его параметрам. '
                                      f'Чтобы узнать, что я умею используй команду /help')


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
    buttons = [types.KeyboardButton(str(button_text)) for button_text in models_dict]
    user_markup.add(*buttons, row_width=len(models_dict))
    bot.send_message(message.chat.id, "Выберите интересующую модель.", reply_markup=user_markup)


def cmd_models_info_link(message):
    if message.text in models_dict:
        response = 'Перейти по ссылке scikit-learn и узнать о модели ' + message.text.lower() + ': ' + models_dict[
            message.text]
        return response
    else:
        return False


@bot.message_handler(content_types=["text"])
def cmd_models_info_reply(message):
    remove_keyboard = types.ReplyKeyboardRemove(selective=False)
    if cmd_models_info_link(message):
        bot.send_message(message.chat.id, cmd_models_info_link(message), reply_markup=remove_keyboard)
    else:
        bot.send_message(message.chat.id, "Выберите представленную модель из списка.")


bot.infinity_polling()
