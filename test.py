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
        nick = mes[20:]
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
    if mes.split()[0] == "common" or mes.split()[0] == "rare" or mes.split()[0] == "epic" or mes.split()[0] == "legendary" or mes.split()[0] == "mythical":
        add_chest(message)


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_query(callback):
    global invent
    global i_nick
    i_nick = search(callback.message.chat.id)
    bot.delete_message(callback.message.chat.id, callback.message.id)
    if callback.data[:4] == "sell":
        bot.send_message(callback.message.chat.id, f"""Вы продали {callback.data[4:]}""")
        invent["inventar"][i_nick]["many"] += market[ingredient_property[callback.data[4:]]['quality']] // 3
        g = f"{callback.data[4:]}-{ingredient_property[callback.data[4:]]['quality']}"
        print(g)
        p = (invent["inventar"][i_nick]["items"]).index(g)
        del invent["inventar"][i_nick]["items"][p]
        bot.send_message(callback.message.chat.id, f"У вас {invent['inventar'][i_nick]['many']} минет")
        main_menu()
    if callback.data == "common-Сундук" or callback.data == "rare-Сундук" or callback.data == "epic-Сундук" or callback.data == "legendary-Сундук" or callback.data == "mythical-Сундук":
        open_chest(callback)
    elif (callback.data.split('-'))[0] in ingredient:
        add_ingredient(callback)
    elif callback.data in burger_update:
        choice_ingredient(callback)
    elif callback.data in add_cutlet:
        add_burger(callback)
    elif callback.data[:11] == "description":
        bot.send_message(callback.message.chat.id, ingredient_property[callback.data[11:]]["description"])
    elif "Булука 🥖" in callback.data:
        bot.send_message(callback.message.chat.id, f"""C Булкой нельзя взаимодействовать""")
        id_1 = str(callback.message.chat.id)
        id_2 = inf[str(id_1)][0]
        value = inf[str(id_1)][1]
        id_fight = inf[str(id_1)][2]
        ingred_1 = inf[str(id_1)][3]
        ingredient[inf[id_1][-1]]["skill"][0](id_fight, value, id_1, id_2, ingred_1)
    elif callback.data[:12] == "place attack":
        damage_play(callback.from_user.id, callback.data[12:])
    elif callback.data[:10] == "place heal":
        heal_play(callback.from_user.id, callback.data[10:])
    elif callback.data[:11] == "place armor":
        armor_play(callback.from_user.id, callback.data[11:])
    elif callback.data[:10] == "place fire":
        fire_play(callback.from_user.id, callback.data[10:])
    elif callback.data[:10] == "place prov":
        god_play(callback.from_user.id, callback.data[10:])
    elif callback.data[:10] == "place copy":
        copy_play(callback.from_user.id, callback.data[10:])
    elif callback.data[:12] == "place snipe1":
        snipe_play(callback.from_user.id, callback.data[12:])
    elif callback.data[:12] == "place snipe2":
        snipe_2_play(callback.from_user.id, callback.data[12:])





# Выход из аккаунта
def quit_message(message):
    connection = sqlite3.connect('Users.db', check_same_thread=False)
    cursor = connection.cursor()
    g = cursor.execute(f"""SELECT user_id FROM User_id_nick""").fetchall()
    s = [g[i][0] for i in range(len(g))]
    cursor.execute(
        f"""UPDATE User_id_nick SET nick = '{message.from_user.id}' WHERE user_id = '{message.from_user.id}'""")
    connection.commit()
    connection.close()
    bot.send_message(message.chat.id, f"""Вы вышли из своего аккаунта""")
    start_message(message)



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
