
import requests
import telebot
from telebot import types
import random
from config import API_KEY, TOKEN

bot = telebot.TeleBot(TOKEN)

# Функция для отправки запроса к Unsplash API
def search_images(query):
    api_key = API_KEY
    url = 'https://api.unsplash.com/search/photos'
    # Параметры запроса
    params = {
        'query': query,
        'client_id': api_key,
        'per_page': 9  # количество возвращаемых изображений
    }

    # Отправляем GET-запрос к API Unsplash
    response = requests.get(url, params=params)

    # Обрабатываем ответ
    if response.status_code == 200:
        # Получаем список URL изображений из ответа
        data = response.json()
        image_urls = [result['urls']['small'] for result in data['results']]

        # Возвращаем список URL изображений
        return image_urls
    else:
        # Обработка ошибки
        return None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(row_width=4)

    # Добавляем на клавиатуру 16 кнопок с эмодзи и категориями
    buttons = [
        types.KeyboardButton('Дети'),
        types.KeyboardButton('Цветы'),
        types.KeyboardButton('Еда'),
        types.KeyboardButton('Природа'),
        types.KeyboardButton('Животные'),
        types.KeyboardButton('Города'),
        types.KeyboardButton('Спорт'),
        types.KeyboardButton('Искусство'),
        types.KeyboardButton('Мотоцикл'),
        types.KeyboardButton('Книги'),
        types.KeyboardButton('Фильмы'),
        types.KeyboardButton('Музыка'),
        types.KeyboardButton('Автомобиль'),
        types.KeyboardButton('Девушки'),
        types.KeyboardButton('Космос'),
        types.KeyboardButton('Мужчины')
    ]
    keyboard.add(*buttons)

    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=keyboard)

# Обработчик сообщений с текстом
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # Ищем изображения на основе текста сообщения
    query = message.text
    image_urls = search_images(query)

    if image_urls is not None:
        # Создаем клавиатуру с вариантами изображений
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        buttons = [types.InlineKeyboardButton('{}'.format(i+1), callback_data='image_{}_{}'.format(query, i)) for i in range(len(image_urls))]
        keyboard.add(*buttons)

        # Отправляем сообщение с вариантами изображений
        bot.send_message(message.chat.id, 'Выберите изображение:', reply_markup=keyboard)
    else:
        # Отправляем сообщение об ошибке
        bot.send_message(message.chat.id, 'Произошла ошибка при поиске изображений')

# Обработчик нажатий на кнопки с вариантами изображений
@bot.callback_query_handler(func=lambda call: call.data.startswith('image_'))
def handle_image_selection(call):
    # Получаем информацию о выбранном изображении
    query, image_number = call.data.split('_')[1], int(call.data.split('_')[2])

    # Отправляем выбранное изображение пользователю
    bot.send_photo(call.message.chat.id, search_images(query)[image_number-1])

# Запускаем бота
bot.polling()
