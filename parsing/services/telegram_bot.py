import telebot
from telebot import types
from config.settings import BOT_TOKEN
from parsing.services.services import GetProblems
from parsing.models import Subscriptions


bot = telebot.TeleBot(BOT_TOKEN)
subscriptions = {}


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    # Создаем объект клавиатуры
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    bot.reply_to(message, f"""\
Привет, {message.chat.first_name}!
Вы можете подписаться на ежедневную рассылку задач с сайта https://codeforces.com
для этого выберите тему и сложность задачи.
/unsubscribe - подписаться
/subscribe - отписаться
/status - статус подписки
/tags - список тем
/level - уровень\
""")


# Handle '/tags'
@bot.message_handler(commands=['tags'])
def send_tags(message):
    tags = GetProblems().get_all_tags()
    text = ""
    for tag in tags:
        text += "/" + str(tag) + "\n"
    bot.reply_to(message, text)


# Handle '/level'
@bot.message_handler(commands=['level'])
def send_level(message):
    contests = GetProblems().get_all_levels()
    text = ""
    for contest in contests:
        text += str(contest) + " " + contest.annotation + " \n"
    bot.reply_to(message, text)


# Handle '/status'
@bot.message_handler(commands=['status'])
def send_status(message):
    text = ""
    subs = GetProblems().get_all_subsriptions(chat_id=message.chat.id)
    if subs.exists():
        text = "У вас нет подписок"
    else:
        for sub in subs:
            text += str(sub) + "\n"
    bot.reply_to(message, text)


# Handle '/subscribe'
@bot.message_handler(commands=['subscribe'])
def send_subscribe(message):
    print("\nmessage.chat.id=", message.chat.id, "\n")
    text = ""
    # subs = GetProblems().make_subsriptions(chat_id=message.chat.id)
    # if isinstance(subs, str):
    #     text = subs
    # elif subs is None:
    #     text = "У вас нет подписок"
    # else:
    #     for sub in subs:
    #         text += str(sub) + "\n"
     # Получение текста сообщения
    text_m = message.text.lower()
    print("text_m=", text_m)

    # Проверка наличия ключевых слов
    if 'тема' in text_m and message.chat.id in subscriptions:
        # Получение выбранной темы
        tema = text_m.split('тема ')[1]
        print("tema=", tema)
        # Добавление выбранной темы в подписку пользователя
        subscriptions[message.chat.id]['tema'] = tema

        # Отправка сообщения с вопросом об уровне
        bot.send_message(message.chat.id, "Введите уровень для подписки:")

    elif 'уровень' in text_m and message.chat.id in subscriptions:
        # Получение выбранного уровня
        uroven = text_m.split('уровень ')[1]
        print("uroven=", uroven )
        # Добавление выбранного уровня в подписку пользователя
        subscriptions[message.chat.id]['uroven'] = uroven

        # Отправка сообщения с вопросом о рейтинге
        bot.send_message(message.chat.id, "Введите рейтинг для подписки:")

    elif 'рейтинг' in text_m and message.chat.id in subscriptions:
        # Получение выбранного рейтинга
        rating = text_m.split('рейтинг ')[1]
        print("rating=", rating)
        # Добавление выбранного рейтинга в подписку пользователя
        subscriptions[message.chat.id]['rating'] = rating

        # Отправка пользователю подтверждения подписки
        bot.send_message(message.chat.id, f"Вы успешно подписались на рассылку!{subscriptions}")

        # Очистка подписки пользователя
        subscriptions[message.chat.id] = {}

    bot.reply_to(message, text)


# Handle '/unsubscribe'
@bot.message_handler(commands=['unsubscribe'])
def send_unsubscribe(message):
    GetProblems().del_all_subsriptions(chat_id=message.chat.id)
    text = "Подписки удалены\n"
    bot.reply_to(message, text)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


def run_bot():
    bot.infinity_polling()


#     # Определяем обработчик команды /start
# @bot.message_handler(commands=['start'])
# def start(message):
#     # Создаем объект клавиатуры
#     keyboard = types.InlineKeyboardMarkup(row_width=3)

#     # Генерируем кнопки для тэгов
#     tags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9', 'tag10',
#             'tag11', 'tag12', 'tag13', 'tag14', 'tag15', 'tag16', 'tag17', 'tag18', 'tag19', 'tag20',
#             'tag21', 'tag22', 'tag23', 'tag24', 'tag25', 'tag26', 'tag27', 'tag28', 'tag29', 'tag30',
#             'tag31', 'tag32', 'tag33', 'tag34', 'tag35', 'tag36', 'tag37']

#     # Добавляем кнопки для каждого тэга
#     for tag in tags:
#         keyboard.add(types.InlineKeyboardButton(tag, callback_data=tag))

#     # Отправляем клавиатуру пользователю
#     bot.send_message(message.chat.id, 'Выберите тэг:', reply_markup=keyboard)

# # Определяем обработчик события нажатия на кнопку
# @bot.callback_query_handler(func=lambda call: True)
# def handle_button_click(call):
#     # Обрабатываем нажатие на кнопку
#     if call.data == 'tag1':
#         # Ваш код при выборе тэга tag1
#         pass
#     elif call.data == 'tag2':
#         # Ваш код при выборе тэга tag2
#         pass
#     # Добавьте обработку для остальных тэгов...
