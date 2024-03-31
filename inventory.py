from config import *
from main import main_menu
from db_operations import search


def inventory_call(message):
    i_nick = search(message.from_user.id)
    if len(invent["inventar"][i_nick]["chests"]) == 0 and len(invent["inventar"][i_nick]["items"]) == 0:
        bot.send_message(message.chat.id, "Ваш инвентарь пуст")
    else:
        for q in invent["inventar"][i_nick]["chests"]:
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton(text="Открыть сундук", callback_data=q)
            markup.add(btn)
            bot.send_message(message.chat.id, q, reply_markup=markup)
        for q in invent["inventar"][i_nick]["items"]:
            bot.send_message(message.chat.id, q)


def my_burger(message):
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


def change_burger(message):
    i_nick = search(message.from_user.id)
    if len(invent["inventar"][i_nick]["items"]) == 0:
        bot.send_message(message.chat.id,
                         "К сожалению у вас не ничего, что можно было бы добавить в бургер. Открывайте кейсы, что бы получить новые ингридиенты!")
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        g = 0
        for i in invent["inventar"][i_nick]["burger"]:
            g += 1
            btn = types.InlineKeyboardButton(text=f"{g}: {i}", callback_data=f"{g} place")
            markup.add(btn)
        bot.send_message(message.chat.id, "Вот куда вы можите добавить ингридиент", reply_markup=markup)


def remake_burger(message):
    i_nick = search(message.from_user.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in invent["inventar"][i_nick]["burger"]:
        if i in all_i:
            invent["inventar"][i_nick]["items"].append(i)
    invent["inventar"][i_nick]["burger"] = clean_burger
    g = 0

    for i in invent["inventar"][i_nick]["burger"]:
        g += 1
        btn = types.InlineKeyboardButton(text=f"{g}: {i}", callback_data=f"{g} place_k")
        markup.add(btn)
    bot.send_message(message.chat.id, "Вот куда вы можите добавить котлету", reply_markup=markup)

def add_chest(message):
    i_nick = search(message.from_user.id)
    markup = main_menu()
    g = message.text
    if i_nick in invent["inventar"]:
        invent["inventar"][i_nick]["chests"].append(g + '-' + "Сундук")
    else:
        invent["inventar"][i_nick] = {"chests": [g + '-' + "Сундук"], "items": [],
                                      "burger": burger}

    bot.send_message(message.chat.id, g + '-' + "Сундук", reply_markup=markup)


def add_ingredient(callback):
    markup = main_menu()
    i_nick = search(callback.message.chat.id)
    if invent["inventar"][i_nick]["burger"][int(callback.data[-1]) - 1] == "Булука 🥖":
        bot.send_message(callback.message.chat.id, "Булку нельзя убрать или поменять", reply_markup=markup)
    elif invent["inventar"][i_nick]["burger"][int(callback.data[-1]) - 1] == "Котлета 🟤":
        bot.send_message(callback.message.chat.id,
                         "Котлету нельзя убрать, что бы её переместить пересобирите бургер", reply_markup=markup)
    else:
        p = (invent["inventar"][i_nick]["items"]).index(callback.data[:-1])
        del invent["inventar"][i_nick]["items"][p]
        if invent["inventar"][i_nick]["burger"][int(callback.data[-1]) - 1] != "":
            invent["inventar"][i_nick]["items"].append(invent["inventar"][i_nick]["burger"][int(callback.data[-1]) - 1])
            bot.send_message(callback.message.chat.id,
                             f"Старый ингридиент: {invent['inventar'][i_nick]['burger'][int(callback.data[-1]) - 1]} перемещён в инвентарь")
        invent["inventar"][i_nick]["burger"][int(callback.data[-1]) - 1] = (callback.data.split('-'))[0]
        bot.delete_message(callback.message.chat.id, callback.message.id)
        bot.send_message(callback.message.chat.id, f"Ингридиент: {callback.data[:-1]} добавлен в бургер",
                         reply_markup=markup)


def choice_ingredient(callback):
    i_nick = search(callback.message.chat.id)
    if invent["inventar"][i_nick]["burger"][int(callback.data[0]) - 1] == "Булука 🥖":
        bot.send_message(callback.message.chat.id, "Булку нельзя убрать или поменять")
    elif invent["inventar"][i_nick]["burger"][int(callback.data[0]) - 1] == "Котлета 🟤":
        bot.send_message(callback.message.chat.id,
                         "Котлету нельзя убрать, что бы её переместить пересобирите бургер")
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in invent["inventar"][i_nick]["items"]:
            btn = types.InlineKeyboardButton(text=f"Добавить {i}➕", callback_data=i + callback.data[0])
            markup.add(btn)

        bot.send_message(callback.message.chat.id, "Вот что вы можите в него добавить", reply_markup=markup)


def add_burger(callback):
    markup = main_menu()
    i_nick = search(callback.message.chat.id)
    if invent["inventar"][i_nick]["burger"][int(callback.data[0]) - 1] == "Булука 🥖":
        bot.send_message(callback.message.chat.id, "Булку нельзя убрать или поменять", reply_markup=markup)
    else:
        invent["inventar"][i_nick]["burger"][int(callback.data[0]) - 1] = "Котлета 🟤"
        bot.delete_message(callback.message.chat.id, callback.message.id)
        bot.send_message(callback.message.chat.id, f"Котлета в Бургере",
                         reply_markup=markup)