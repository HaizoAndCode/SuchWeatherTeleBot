from telebot import types
import telebot
import requests
import json



# token and api
bot = telebot.TeleBot('your token')
API = 'your api on OpenWeather'
# 
city_names = [
    "Москва",
    "Санкт-Петербург",
    "Новосибирск",
    # Add more city names here
]

keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
for city_name in city_names:
    button = types.KeyboardButton(city_name)
    keyboard.add(button)


# Start
@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}! Выберите название одного из городов или напишите название своего города.', reply_markup=keyboard)

weather_translations = {
    "clear sky": "ясное небо",
    "few clouds": "немного облачно",
    "scattered clouds": "разрозненные облака",
    # Добавьте остальные переводы погодных условий по необходимости
}


@bot.message_handler(content_types=['text'])


def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    data = res.json()

    if "name" in data:
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        wind_speed = data["wind"]["speed"]

        if description in weather_translations:
            translated_description = weather_translations[description]
            bot.reply_to(message, f'Сейчас погода: {temperature}°C, {translated_description}. Скорость ветра: {wind_speed} м/с')
        else:
            bot.reply_to(message, f'Сейчас погода: {temperature}°C, {description}. Скорость ветра: {wind_speed} м/с')
    else:
        bot.reply_to(message, 'Город не найден')



@bot.message_handler(content_types=['photo'])
def grt_photo(message):
    markup = types.InlineKeyboardMarkup()  # Создаем новый объект markup для каждого сообщения с фотографией
    btn2 = types.InlineKeyboardButton('Удалить текущее сообщение', callback_data='delet1')
    btn3 = types.InlineKeyboardButton('Удалить фото', callback_data='delete0')
    markup.row(btn2, btn3)
    bot.reply_to(message, 'Мне не нужны фотографии. 😅', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete0':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)  # Удалить предыдущее сообщение
        bot.delete_message(callback.message.chat.id, callback.message.message_id)  # Удалить текущее сообщение
    elif callback.data == 'delet1':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)  # Удалить текущее сообщение









bot.polling(none_stop=True)
