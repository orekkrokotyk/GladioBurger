from config import *
from db_operations import *
from chest import *
# from inventory import *
from inventory import inventory_call, my_burger, change_burger, remake_burger, add_chest, add_ingredient, choice_ingredient, add_burger
from fight_bot import *
from main import main_menu

import telebot
from telebot import types


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"""Добро пожаловать, введите никнейм""")
    bot.register_next_step_handler(message, second_message)


def second_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    find_id = search_nickname(message)
    if len(find_id) == 0:
        size_but_1 = types.KeyboardButton("Другой ник")
        size_but_2 = types.KeyboardButton(f"Регестрация с ником {message.text}")
        markup.add(size_but_1)
        markup.add(size_but_2)
        bot.send_message(message.chat.id, f"""Такого ника не существует, можете ввести новый или зарегестрироваться с этим""", reply_markup=markup)
    else:
        size_but_1 = types.KeyboardButton(f"Вход с ником {message.text}")
        size_but_2 = types.KeyboardButton("Другой ник")
        markup.add(size_but_1)
        markup.add(size_but_2)
        bot.send_message(message.chat.id, f"""Такой ник есть, можите войти или ввести новый""", reply_markup=markup)


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
    if mes[:11] == "Регестрация":
        nick = mes[19:]
        bot.send_message(message.chat.id, f"""Регестрируйся, Придумайте пароль""")
        bot.register_next_step_handler(message, pas, nick)
    elif mes[:4] == "Вход":
        nick = mes[13:]
        bot.send_message(message.chat.id, f"""Введите пароль""")
        bot.register_next_step_handler(message, log_pass, nick)
    elif mes == "Другой ник":
        start_message(message)
    if mes == "Кейсы":
        get_chest(message)
    elif mes == 'Инвентарь':
        inventory_call(message)
    elif mes == "Мой бургер":
        my_burger(message)
    elif mes == "В Бой!":
        wait_list(message)
    if mes == "Изменить этот Бургер":
        change_burger(message)
    elif mes == "Полностью его пересобрать":
        remake_burger(message)
    if mes == "Предъистория мира":
        pass
    elif mes == "Начать обучение":
        pass
    if mes == "common" or mes == "rare" or mes == "epic" or mes == "legendary" or mes == "mythical":
        add_chest(message)
        add_chest(message)
        add_chest(message)
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
        bot.delete_message(callback.message.chat.id, callback.message.id)
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
