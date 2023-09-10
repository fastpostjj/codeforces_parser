from config.settings import BOT_TOKEN
import telebot
from parsing.services.services import GetProblems
from parsing.models import Subscriptions


bot = telebot.TeleBot(BOT_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, f"""\
Привет, {message.chat.first_name}!
Вы можете подписаться на ежедневную рассылку задач с сайта https://codeforces.com
для этого выберите тему и сложность задачи.
/subscribe - подписаться
/status - статус подписки
/tags - список тем
/level - уровень\
""")


# Handle '/tags'
@bot.message_handler(commands=['tags'])
def send_tags(message):
    tags = GetProblems.get_all_tags()
    text = ""
    for tag in tags:
        text += "/" + str(tag) + "\n"
    bot.reply_to(message, text)


# Handle '/level'
@bot.message_handler(commands=['level'])
def send_level(message):
    contests = GetProblems.get_all_levels()
    text = ""
    for contest in contests:
        text += str(contest) + " " + contest.annotation + " \n"
    bot.reply_to(message, text)


# Handle '/subscribe'
@bot.message_handler(commands=['subscribe'])
def send_subscribe(message):
    print("\nmessage.chat.id=", message.chat.id, "\n")
    text = ""
    subs = GetProblems().make_subsriptions(chat_id=message.chat.id)
    if isinstance(subs, str):
        text = subs
    elif subs is None:
        text = "У вас нет подписок"
    else:
        for sub in subs:
            text += str(sub) + "\n"
    bot.reply_to(message, text)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


def run_bot():
    bot.infinity_polling()
