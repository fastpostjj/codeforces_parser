import telebot
from config.settings import BOT_TOKEN
from parsing.services.services import GetProblems


bot = telebot.TeleBot(BOT_TOKEN)
subscriptions = {}


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, f"""\
Привет, {message.chat.first_name}!
Вы можете подписаться на ежедневную рассылку задач с сайта https://codeforces.com
для этого укажите тему, рейтинг и уровень сложности задач.
/subscribe тема <тема> рейтинг <рейтинг> уровень <уровень>
/unsubscribe - отписаться
/status - статус подписки
/tags - список тем
/level - уровень
/rating - значения рейтинга
/sample - шаблон для подписки\
""")


# Handle '/tags'
@bot.message_handler(commands=['tags'])
def send_tags(message):
    tags = GetProblems().get_all_tags()
    text = ""
    for tag in tags:
        text += str(tag.id) + " " + str(tag) + "\n"
    bot.reply_to(message, text)


# Handle '/rating'
@bot.message_handler(commands=['rating'])
def send_rating(message):
    ratings = GetProblems().get_all_rating()
    text = ""
    for rating in ratings:
        text += str(rating) + " "
    text += "\n"
    bot.reply_to(message, text)


# Handle '/level'
@bot.message_handler(commands=['level'])
def send_level(message):
    contests = GetProblems().get_all_levels()
    text = ""
    for contest in contests:
        text += str(contest) + " " + str(contest.annotation) + " \n"
    bot.reply_to(message, text)


# Handle '/sample'
@bot.message_handler(commands=['sample'])
def send_sample(message):
    text = "Для того, чтобы создать подписку, отправьте сообщение с номером тега, рейтингом (не обязательно) и уровнем сложности:\n" +\
        "/subscribe тема <номер тега> рейтинг <рейтинг> уровень <уровень>"
    bot.reply_to(message, text)


# Handle '/status'
@bot.message_handler(commands=['status'])
def send_status(message):
    text = "Ваши подписки\n"
    subs = GetProblems().get_all_subscriptions(chat_id=message.chat.id)
    if not subs.exists():
        text = "У вас нет подписок"
    else:
        for sub in subs:
            text += str(sub) + "\n"
    bot.reply_to(message, text)


# Handle '/subscribe'
@bot.message_handler(commands=['subscribe'])
def send_subscribe(message):
    getproblems = GetProblems()
    # Получение текста сообщения
    text = message.text.lower()
    subscriptions = getproblems.get_sub_from_str(text)
    subscriptions['chat_id'] = message.chat.id

    # проверяем корректность задания подписки
    if getproblems.check_subscriptions(subscriptions):
        if getproblems.is_subscriptions_exists(subscriptions):
            bot.send_message(
                message.chat.id,
                "Такая подписка уже существует.")
        else:
            new_sub = getproblems.make_subscriptions(subscriptions)
            # Отправка пользователю подтверждения подписки
            bot.send_message(
                message.chat.id,
                f"Вы успешно подписались на рассылку!\n{new_sub}")
    else:
        bot.send_message(
            message.chat.id,
            "Ошибка при создании подписки. Попробуйте еще.")

    # Очистка словаря
    subscriptions = {}


# Handle '/unsubscribe'
@bot.message_handler(commands=['unsubscribe'])
def send_unsubscribe(message):
    GetProblems().del_all_subscriptions(chat_id=message.chat.id)
    text = "Подписки удалены\n"
    bot.reply_to(message, text)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "Хм... не знаю, что сказать на это\n")


def run_bot():
    bot.infinity_polling()
