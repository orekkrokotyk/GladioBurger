from config import *
from db_operations import *
from chest import *
# from inventory import *
from inventory import inventory_call, my_burger, change_burger, remake_burger, add_chest, add_ingredient, choice_ingredient, add_burger
from fight import *
from main import main_menu

import telebot
from telebot import types


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    size_but_1 = types.KeyboardButton("Вход")
    size_but_2 = types.KeyboardButton("Регестрация")
    markup.add(size_but_1)
    markup.add(size_but_2)
    bot.send_message(message.chat.id, f"""Добро пожаловать""", reply_markup=markup)


@bot.message_handler(commands=['quit'])
def bot_quit_message(message):
    quit_message(message)

@bot.message_handler(content_types=['text'])
def func(message):
    global i_nick
    global invent
    global figh
    mes = message.text
    if mes == 'Главное меню':
        markup = main_menu()
        bot.send_message(message.chat.id, f"""Вы в главном меню игры""", reply_markup=markup)
    if mes == "Регестрация":
        msg = bot.send_message(message.chat.id, f"""Регестрируйся, Реальное имя""")
        bot.register_next_step_handler(msg, name)
    elif message.text == "Вход":
        msg = bot.send_message(message.chat.id, f"""Введите свой ник""")
        bot.register_next_step_handler(msg, log_nick)
    if mes == "Кейсы":
        get_chest(message)
    elif mes == 'Инвентарь':
        inventory_call(message)
    elif mes == "Мой бургер":
        my_burger(message)
    elif mes == "В Бой!":
        waiting_list(message)
    if mes == "Изменить этот Бургер":
        change_burger(message)
    elif mes == "Полностью его пересобрать":
        remake_burger(message)
    if mes == "common" or mes == "rare" or mes == "epic" or mes == "legendary" or mes == "mythical":
        add_chest(message)


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_query(callback):
    global invent
    global i_nick
    i_nick = search(callback.message.chat.id)
    if callback.data == "common-Сундук" or callback.data == "rare-Сундук" or callback.data == "epic-Сундук" or callback.data == "legendary-Сундук" or callback.data == "mythical-Сундук":
        open_chest(callback)
    elif (callback.data.split('-'))[0] in ingredient:
        add_ingredient(callback)
    elif callback.data in burger_update:
        choice_ingredient(callback)
    elif callback.data in add_cutlet:
        add_burger(callback)
    elif callback.data[:12] == "place attack":
        damage_play(callback.from_user.id, callback.data[12:])
    elif callback.data[:10] == "place heal":
        heal_play(callback.from_user.id, callback.data[10:])
    elif callback.data[:11] == "place armor":
        armor_play(callback.from_user.id, callback.data[11:])
    elif callback.data[:10] == "place fire":
        fire_play(callback.from_user.id, callback.data[10:])


def exit_handler():
    with open("invent_data.json", 'w', encoding="utf-8") as fp:
        json.dump(invent, fp, ensure_ascii=False)
        fp.close()
    with open("fight_data.json", 'w', encoding="utf-8") as fp:
        json.dump(figh, fp, ensure_ascii=False)
        fp.close()
    f = open("burger_data.json", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()
    f = open("end_turn.json", 'w', encoding='utf8')
    json.dump(e_t, f, ensure_ascii=False)
    f.close()
    print('ЖОПА')


atexit.register(exit_handler)

bot.infinity_polling()
