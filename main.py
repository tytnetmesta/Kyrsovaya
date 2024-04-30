import telebot
from telebot import types
import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("6585561489:AAHxIXhBrrckVyKGFmokcReV8ShtrneUwSk")
ADMIN_CHAT_ID = -4148678242

operators = {
    "Тимур": "@tytnetmesta0"
}

NOTIFICATION_CHAT_ID = "-4148678242"

request_chat_ids = {}
user_last_action = {}

user_last_request_time = {}

REQUEST_LIMIT_INTERVAL = 5


bot = telebot.TeleBot("6585561489:AAHxIXhBrrckVyKGFmokcReV8ShtrneUwSk")

operators = {
    "Тимур": "@tytnetmesta0",
    "Никита": "@duvetqwe",
    "Давид": "@DaBabyshka"
}

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    try:
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        start_button = types.KeyboardButton('Старт')
        keyboard.add(start_button)

        bot.send_message(message.chat.id, "Для начала работы нажмите кнопку 'Старт'.", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

@bot.message_handler(func=lambda message: message.text == 'Старт')
def handle_start_button(message):
    try:
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = [
            'Оформить обращение', 'Связаться с оператором', 'Оценить качество обслуживания',
            'Получить контактные данные', 'Получить информацию о товарах'
        ]
        keyboard.add(*[types.KeyboardButton(button) for button in buttons])

        bot.send_message(message.chat.id, "Выберите нужную опцию:", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

# Обработчик команды /reply
@bot.message_handler(commands=['reply'])
def handle_reply_command(message):
    command_parts = message.text.split(maxsplit=2)
    if len(command_parts) >= 3:
        try:
            reply_to_message_id = int(command_parts[1])
            response_text = command_parts[2]
            if reply_to_message_id in request_chat_ids:
                original_chat_id = request_chat_ids[reply_to_message_id]['user_id']
                bot.send_message(original_chat_id, response_text)
                bot.send_message(message.chat.id, "Ответ отправлен пользователю.")
                # Удаляем информацию об обращении
                del request_chat_ids[reply_to_message_id]
            else:
                bot.send_message(message.chat.id, f"Данного ID не существует {reply_to_message_id}")
        except ValueError:
            bot.send_message(message.chat.id, "Используйте /reply с идентификатором и текстом.")
    else:
        bot.send_message(message.chat.id, "Используйте /reply с идентификатором и текстом.")


# Обработчик нажатия кнопки "Оформить обращение"
@bot.message_handler(func=lambda message: message.text == 'Оформить обращение')
def handle_request_creation(message):
    try:
        user_last_action[message.chat.id] = 'Оформить обращение'

        hide_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Пожалуйста, напишите ваше обращение с помощью команды /request.", reply_markup=hide_markup)

        bot.send_message(message.chat.id, "Ваше обращение получено. Ожидайте ответа.")

        back_button = types.KeyboardButton('Назад')
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(back_button)
        bot.send_message(message.chat.id, "Для возврата в меню нажмите кнопку 'Назад'.", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

# Обработчик всех сообщений после нажатия кнопки "Оформить обращение"
@bot.message_handler(func=lambda message: user_last_action.get(message.chat.id) == 'Оформить обращение')
def handle_any_message_after_request_creation(message):
    try:
        del user_last_action[message.chat.id]

        back_button = types.KeyboardButton('Назад')
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(back_button)
        bot.send_message(message.chat.id, "Для возврата в меню нажмите кнопку 'Назад'.", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_menu')
def back_to_menu_callback(call):
    handle_start_button(call.message)

@bot.message_handler(func=lambda message: message.text == 'Назад')
def handle_back_button(message):
    if message.chat.id in user_last_action:
        del user_last_action[message.chat.id]

    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=generate_main_menu())


# Обработчик нажатия кнопки "Оценить качество обслуживания"
@bot.message_handler(func=lambda message: message.text == 'Оценить качество обслуживания')
def handle_rate_service(message):
    try:
        user_last_action[message.chat.id] = 'Оценить качество обслуживания'

        reply_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        reply_markup.add(*[types.KeyboardButton(str(i)) for i in range(1, 11)])
        bot.send_message(message.chat.id, "Оцените качество обслуживания (от 1 до 10):", reply_markup=reply_markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

# Обработчик нажатия на оценку качества обслуживания
@bot.message_handler(func=lambda message: message.text in [str(i) for i in range(1, 11)])
def handle_service_rating(message):
    try:
        if user_last_action.get(message.chat.id) == 'Оценить качество обслуживания':
            rating = message.text

            bot.send_message(message.chat.id, "Оставьте комментарий или нажмите 'Назад' для возвращения в меню.",
                             reply_markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                             .add(types.KeyboardButton('Назад')))

            user_last_action[message.chat.id] = {'action': 'Помогли ли мы вам?', 'rating': rating}
        else:
            bot.send_message(message.chat.id,
                             "Неверная команда. Пожалуйста, выберите кнопку 'Оценить качество обслуживания'.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


# Обработчик нажатия на комментарий или кнопку "Назад"
@bot.message_handler(func=lambda message: user_last_action.get(message.chat.id) and user_last_action[message.chat.id]['action'] == 'Помогли ли мы вам?')
def handle_comment_or_back(message):
    try:
        if message.text.lower() == 'назад':
            handle_start_button(message)
        else:
            if 'rating' in user_last_action[message.chat.id]:
                rating = user_last_action[message.chat.id]['rating']
                comment = message.text

                del user_last_action[message.chat.id]

                handle_start_button(message)
            else:
                bot.send_message(message.chat.id, "Чтобы оставить комментарий, сначала оцените качество обслуживания.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


# Обработчик нажатия кнопки "Связаться с оператором"
@bot.message_handler(func=lambda message: message.text == 'Связаться с оператором')
def handle_contact_operator(message):
    try:
        operator_username = operators.get("Тимур")

        keyboard = types.InlineKeyboardMarkup()
        operator_button = types.InlineKeyboardButton(text="Связаться с Тимуром", url="https://t.me/tytnetmesta0")
        keyboard.add(operator_button)

        bot.send_message(message.chat.id, "Свяжитесь с оператором Тимуром:", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


# Обработчик нажатия кнопки "Получить контактную информацию"
@bot.message_handler(func=lambda message: message.text == 'Получить контактные данные')
def handle_contact_info(message):
    try:
        bot.delete_message(message.chat.id, message.message_id - 1)

        keyboard = types.InlineKeyboardMarkup()
        facebook_button = types.InlineKeyboardButton("VK", url="https://vk.com/tytnetmesta")
        twitter_button = types.InlineKeyboardButton("Reddit", url="https://www.reddit.com/user/Evangeline145/")
        instagram_button = types.InlineKeyboardButton("Instagram", url="https://www.instagram.com/tytnetmesta___?igsh=OGdoMmVkc3Fqb2Qw&utm_source=qr")
        youtube_button = types.InlineKeyboardButton("YouTube", url="https://www.youtube.com/channel/UCj6Sy0Uyn0PungHFl2sDyog")
        back_button = types.InlineKeyboardButton('Назад', callback_data='back_to_menu_contact_info')

        keyboard.add(facebook_button, twitter_button, instagram_button, youtube_button, back_button)

        bot.send_message(message.chat.id, "Выберите социальную сеть для контакта:", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_menu_contact_info')
def back_to_menu_contact_info_callback(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)

        bot.send_message(call.message.chat.id, "Выберите опцию:", reply_markup=generate_main_menu())
    except Exception as e:
        print(f"Произошла ошибка при удалении сообщения или отправке нового сообщения: {e}")


def generate_main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        'Оформить обращение', 'Связаться с оператором', 'Оценить качество обслуживания',
        'Получить контактные данные', 'Получить информацию о товарах'
    ]
    keyboard.add(*[types.KeyboardButton(button) for button in buttons])
    return keyboard


# Обработчик нажатия кнопки "Получить информацию о товарах"
@bot.message_handler(func=lambda message: message.text == 'Получить информацию о товарах')
def handle_product_info(message):
    try:
        bot.delete_message(message.chat.id, message.message_id - 1)

        keyboard = types.InlineKeyboardMarkup(row_width=1)

        products = [
            {"name": "Тариф 1", "price": "300 руб./месяц",
             "description": "Тариф 1 предоставляет скорость интернета 50 мбит/с и 1 тб турбо трафика. Подходит как для повседневного использования, так и для потокового просмотра видео.",
             "manager": "@tytnetmesta0"},
            {"name": "Тариф 2", "price": "400 руб./месяц",
             "description": "Тариф 2 предоставляет скорость интернета 75 мбит/с и 2 тб турбо трафика. Идеально подходит для просмотра видео в HD-качестве и онлайн-игр.",
             "manager": "@tytnetmesta0"},
            {"name": "Тариф 3", "price": "500 руб./месяц",
             "description": "Тариф 3 предоставляет скорость интернета 100 мбит/с и 3 тб турбо трафика. Подходит для работы, развлечений и потокового просмотра мультимедийного контента.",
             "manager": "@tytnetmesta0"},
            {"name": "Тариф 4", "price": "750 руб./месяц",
             "description": "Тариф 4 предоставляет скорость интернета 150 мбит/с и 5 тб турбо трафика. Идеально подходит для семейного использования и онлайн-игр.",
             "manager": "@tytnetmesta0"},
            {"name": "Тариф 5", "price": "1000 руб./месяц",
             "description": "Тариф 5 предоставляет скорость интернета 250 мбит/с и безлимитный турбо трафик. Подходит для профессиональных пользователей и стриминговых сервисов.",
             "manager": "@tytnetmesta0"},
            {"name": "Тариф 6", "price": "1500 руб./месяц",
             "description": "Тариф 6 предоставляет скорость интернета 300 мбит/с и безлимитный турбо трафик. Подходит для требовательных задач и высокоскоростного потокового видео.",
             "manager": "@tytnetmesta0"}
        ]

        for product in products:
            product_button = types.InlineKeyboardButton(
                text=f"{product['name']} - {product['price']}",
                callback_data=f"product_{product['name']}"
            )
            keyboard.add(product_button)

        # Добавляем кнопку "Назад" для возврата в обычное меню
        back_button = types.InlineKeyboardButton('Назад', callback_data='back_to_main_menu')
        keyboard.add(back_button)

        # Отправляем сообщение с клавиатурой
        bot.send_message(message.chat.id, "Выберите тариф интернета:", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


# Обработчик для нажатия на кнопку товара
@bot.callback_query_handler(func=lambda call: call.data.startswith('product_'))
def handle_product_selection(call):
    try:
        product_name = call.data.split('_')[1]

        manager_button = types.InlineKeyboardButton(
            text="Связаться с менеджером",
            url=f"https://t.me/@tytnetmesta0"
        )
        back_button = types.InlineKeyboardButton('Назад', callback_data='back_to_product_list')
        keyboard = types.InlineKeyboardMarkup().add(manager_button, back_button)

        # Отправляем сообщение с полной информацией о товаре и кнопками
        if product_name == 'Тариф 1':
            bot.send_message(call.message.chat.id, "Информация о Тарифе 1:\n"
                                                   "Цена: 300 руб./месяц\n"
                                                   "Описание: Тариф 1 предоставляет скорость интернета 50 мбит/с и 1 тб турбо трафика. Подходит как для повседневного использования, так и для потокового просмотра видео.",
                             reply_markup=keyboard)
        elif product_name == 'Тариф 2':
            bot.send_message(call.message.chat.id, "Информация о Тарифе 2:\n"
                                                   "Цена: 400 руб./месяц\n"
                                                   "Описание: Тариф 2 предоставляет скорость интернета 75 мбит/с и 2 тб турбо трафика. Идеально подходит для просмотра видео в HD-качестве и онлайн-игр.",
                             reply_markup=keyboard)
        elif product_name == 'Тариф 3':
            bot.send_message(call.message.chat.id, "Информация о Тарифе 3:\n"
                                                   "Цена: 500 руб./месяц\n"
                                                   "Описание: Тариф 3 предоставляет скорость интернета 100 мбит/с и 3 тб турбо трафика. Подходит для работы, развлечений и потокового просмотра мультимедийного контента.",
                             reply_markup=keyboard)
        elif product_name == 'Тариф 4':
            bot.send_message(call.message.chat.id, "Информация о Тарифе 4:\n"
                                                   "Цена: 750 руб./месяц\n"
                                                   "Описание: Тариф 4 предоставляет скорость интернета 150 мбит/с и 5 тб турбо трафика. Идеально подходит для семейного использования и онлайн-игр.",
                             reply_markup=keyboard)
        elif product_name == 'Тариф 5':
            bot.send_message(call.message.chat.id, "Информация о Тарифе 5:\n"
                                                   "Цена: 1000 руб./месяц\n"
                                                   "Описание: Тариф 5 предоставляет скорость интернета 250 мбит/с и безлимитный турбо трафик. Подходит для профессиональных пользователей и стриминговых сервисов.",
                             reply_markup=keyboard)
        elif product_name == 'Тариф 6':
            bot.send_message(call.message.chat.id, "Информация о Тарифе 6:\n"
                                                   "Цена: 1500 руб./месяц\n"
                                                   "Описание: Тариф 6 предоставляет скорость интернета 300 мбит/с и безлимитный турбо трафик. Подходит для требовательных задач и высокоскоростного потокового видео.",
                             reply_markup=keyboard)

        # Удаляем предыдущее сообщение и кнопки
        if call.message:
            bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {e}")


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_product_list')
def back_to_product_list_callback(call):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        products = [
            {"name": "Тариф 1", "price": "300 руб./месяц"},
            {"name": "Тариф 2", "price": "400 руб./месяц"},
            {"name": "Тариф 3", "price": "500 руб./месяц"},
            {"name": "Тариф 4", "price": "750 руб./месяц"},
            {"name": "Тариф 5", "price": "1000 руб./месяц"},
            {"name": "Тариф 6", "price": "1500 руб./месяц"}
        ]
        for product in products:
            product_button = types.InlineKeyboardButton(
                text=f"{product['name']} - {product['price']}",
                callback_data=f"product_{product['name']}"
            )
            keyboard.add(product_button)
        back_button = types.InlineKeyboardButton('Назад', callback_data='back_to_main_menu')
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите тариф интернета:", reply_markup=keyboard)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main_menu')
def back_to_main_menu_callback(call):
    try:
        bot.send_message(call.message.chat.id, "Выберите опцию:", reply_markup=generate_main_menu())
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запуск бота
bot.infinity_polling()