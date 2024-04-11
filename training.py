import telebot
from telebot import types
from config import *
from inventory import my_burger
from db_operations import search

def training_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    size_but_1 = types.KeyboardButton("Предъистория мира")
    size_but_2 = types.KeyboardButton("Начать обучение")
    markup.add(size_but_1)
    markup.add(size_but_2)
    bot.send_message(message.chat.id,
                     """Добро пожаловать, на кровавую арену смерти, сейчас я введу тебя в курс дела.\n
Если хочешь, могу рассказать тебе предъисторию мира, или сразу переёдём к делу?""",
                     reply_markup=markup)


def training_step_pre_fight(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     """Чтож, перейдём к делу, cейчас ты выйдешь на Арену""",
                     reply_markup=markup)
    bot.send_message(message.chat.id,
                     """Там тебя будет ждать твой первый соперник""")
    bot.send_message(message.chat.id, """Бутерброд""")
    bot.send_message(message.chat.id, """Тебе не стоит боятся, он тренеровочный и не сможет тебя ударить""")
    bot.send_message(message.chat.id, """Чтож боец, как будешь готов нажми на кнопку""")


def training_step_after_fight(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    size_but_1 = types.KeyboardButton("Мой бургер (Тренеровка)")
    markup.add(size_but_1)
    bot.send_message(message.chat.id,
                     """Чтож, перейдём к делу, сейчас у тебя появилявится кнопка «Мой бургер»""",
                     reply_markup=markup)
    bot.send_message(message.chat.id,
                     """Нажми на неё""")


@bot.message_handler(content_types=['text'])
def func(message):
    mes = message.text
    if mes == "Мой бургер (Тренеровка)":
        i_nick = search(message.from_user.id)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        size_but_1 = types.KeyboardButton("Изменить этот Бургер")
        size_but_2 = types.KeyboardButton("Полностью его пересобрать")
        size_but_3 = types.KeyboardButton('Главное меню')

        markup.add(size_but_1)
        markup.add(size_but_2)
        markup.add(size_but_3)
        bot.send_message(message.chat.id, "На данный момент твой бургер выглядит так:", reply_markup=markup)

        for i in invent["inventar"][i_nick]["burger"]:
            if i != "":
                bot.send_message(message.chat.id, i)


def wait_training_list(message, enemy):
    training = [str(message.from_user.id), enemy]

    bot.send_message(message.chat.id, "Вы в списке гладиаторов ожидающих бой")

    war_l = [x for x in figh]
    figh[str(int(war_l[-1]) + 1)] = training[:2]
    del training[:2]

    prep_fight(str(int(war_l[-1]) + 1))
