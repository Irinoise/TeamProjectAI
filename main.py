import telebot
from telebot import types
import pandas as pd

# http://t.me/movies_revenue_prediction_bot

token = '5216695845:AAFwPhtMXamZYg-nF7HqPplgv4KhJvGeW6k'
bot = telebot.TeleBot(token)

data = pd.read_csv('https://www.dropbox.com/s/m7z8uj88smjjhd4/movies_raw_dataset.csv?dl=1')
print(data)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    pass


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id,
                     'Привет! Я помогу тебе разобраться в моей работе. У меня есть следующие команды: \n \n'
                     '/dataset_info - получить информацию о наборе данных \n'
                     '/models_info - получить описание моделей \n'
                     '/show_movie_list - найти фильм по году выпуска')


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


@bot.message_handler(commands=['show_movie_list'])
def cmd_help(message):
    bot.send_message(message.chat.id, 'За какой год увидеть фильмы? Напишите число.')
    bot.register_next_step_handler(message, get_films_by_year_bot)


@bot.message_handler(content_types=["text"])
def cmd_models_info_reply(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id,
                     'Перейти по ссылке scikit-learn и узнать о модели ' + message.text.lower() + ': ' +
                     cmd_models_info_link(
                         message), reply_markup=markup)


data_subset = data['release_date']
data['release_date'] = pd.to_datetime(data['release_date'], format='%m/%d/%y')
data['year'] = data['release_date'].dt.year

data['year'] = data['year'].astype(int)


def get_films_by_year(selected_year):
    selected_data = data[data.year == selected_year]
    return selected_data


def get_films_by_year_bot(message):
    if message.text.isdigit():
        result_list = []
        subset = get_films_by_year(int(message.text)).reset_index()
        if len(subset) < 2:
            bot.send_message(message.chat.id, 'Фильмы за этот год не найдены')
            return
        max_idx = 4
        if len(subset) < max_idx:
            max_idx = len(subset)
        bot.send_message(message.chat.id, 'Я нашел следующие фильмы:')
        for idx in range(1, max_idx):
            print(subset["original_title"][idx])
            result_str = str('*Название фильма: '+ subset["original_title"][idx]) + '*\n\n_Описание фильма: ' + str(subset['overview'][idx]) + '_\n\n'
            result_list.append(result_str)
            bot.send_message(chat_id=message.chat.id, text=result_str, parse_mode='Markdown')

    else:
        bot.send_message(message.chat.id, 'Введите только год (например, 2012)')
        bot.register_next_step_handler(message, get_films_by_year_bot)


bot.infinity_polling()