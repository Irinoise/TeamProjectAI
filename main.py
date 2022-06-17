import telebot
from telebot import types
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

data = pd.read_csv('movies_raw_dataset.csv', parse_dates=[
    'release_date'])
data['release_date'] = pd.to_datetime(data['release_date'], format='%d-%m-%y')
data.loc[data['release_date'].dt.year >= 2021, 'release_date'] -= pd.DateOffset(years=100)
data.drop(columns=['belongs_to_collection', 'id', 'homepage', 'imdb_id', 'original_title', 'spoken_languages', 'status', 'tagline', 'Keywords'], inplace=True)
data.dropna(subset=['genres', 'overview', 'poster_path', 'production_companies', 'production_countries', 'cast', 'crew'], inplace=True)

data_subset = data[['budget', 'popularity', 'runtime', 'revenue', 'title']]
data_subset = data_subset[data_subset['budget'] != 0]

data_subset['release_day'] = data['release_date'].dt.dayofweek + 1
data_subset['release_month'] = data['release_date'].dt.month
data_subset['release_year'] = data['release_date'].dt.year
data_subset = data_subset[['budget', 'popularity', 'runtime', 'revenue', 'release_month', 'release_year']]

y = data_subset['revenue']
X = data_subset.drop(columns=['revenue'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=5)
log_y_train = np.log1p(y_train)
log_y_test = np.log1p(y_test)

categorical_features = ['release_year', 'release_month' ]
numeric_features = ['budget', 'runtime', 'popularity']

column_transformer = ColumnTransformer([
    ('ohe', OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ('scaling', StandardScaler(), numeric_features)
])

regression = RandomForestRegressor(max_depth=2, random_state=10)
pipeline_forest = Pipeline(steps=[
    ('ohe_and_scaling', column_transformer),
    ('regression', regression)
])



def predict_using_random_forest():
    model_with_rand_forest = pipeline_forest.fit(X_train, log_y_train)
    rand_forest_predict = model_with_rand_forest.predict(X_test)
    result = round(np.expm1(rand_forest_predict[-1]), 2)
    return result


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


@bot.message_handler(commands=['predict'])
def cmd_predict(message):
    bot.send_message(message.chat.id, "Введи через пробел бюджет фильма, его популярность (1-100), "
                                      "его продолжительность "
                                      "минутах, месяц (1-12) и год выпуска.")


@bot.message_handler(content_types=['text'])
def predict_revenue(message):
    movie_data = message.text.split(' ')
    X_test.loc[len(X_test)] = movie_data
    print(movie_data)
    print(X_test)
    result = str(predict_using_random_forest())
    bot.send_message(message.chat.id, 'По вашим критериям фильм в прокате соберет $' + result + ' USD')
    if int(float(result)) > 5000000:
        bot.send_message(message.chat.id, 'Фильм снимали в Голливуде? \U0001F632')
    else:
        bot.send_message(message.chat.id, 'Что-то из арт-хауса? \U0001F3A5')


def cmd_models_info_link(message):
    if message.text in models_dict:
        response = 'Перейти по ссылке scikit-learn и узнать о модели ' + message.text.lower() + ': ' + models_dict[
            message.text]
        return response
    else:
        return False

# @bot.message_handler(content_types=["text"])
# def cmd_models_info_reply(message):
#     remove_keyboard = types.ReplyKeyboardRemove(selective=False)
#     if cmd_models_info_link(message):
#         bot.send_message(message.chat.id, cmd_models_info_link(message), reply_markup=remove_keyboard)
    # else:
    #     bot.send_message(message.chat.id, "Выберите представленную модель из списка.")


print(X_test)

bot.infinity_polling()
