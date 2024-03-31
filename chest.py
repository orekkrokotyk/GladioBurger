from config import *
from main import main_menu
from db_operations import search


def get_chest(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('common')
    btn2 = types.KeyboardButton('rare')
    btn3 = types.KeyboardButton('epic')
    btn4 = types.KeyboardButton('legendary')
    btn5 = types.KeyboardButton('mythical')
    btn6 = types.KeyboardButton('Главное меню')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    markup.add(btn6)
    bot.send_message(message.chat.id, 'Какой кейс?', reply_markup=markup)


def open_chest(callback):
    global invent
    i_nick = search(callback.message.chat.id)
    p = (invent["inventar"][i_nick]["chests"]).index(callback.data)
    del invent["inventar"][i_nick]["chests"][p]
    bot.delete_message(callback.message.chat.id, callback.message.id)
    rarity = callback.data[:-7]
    chat_id = callback.message.chat.id
    markup = main_menu()
    for i in range(0, 5):
        for t in range(chests[rarity][i]):
            cr.append(list(ingredients.keys())[i])
    random.shuffle(cr)
    h = cr[random.randint(0, 100)]
    item = random.randint(0, len(ingredients[h]) - 1)
    bot.send_message(chat_id, h + ':')
    bot.send_message(chat_id, ingredients[h][item], reply_markup=markup)
    cr.clear()

    if i_nick in invent["inventar"]:
        invent["inventar"][i_nick]["items"].append(ingredients[h][item] + '-' + h)
    else:
        invent["inventar"][i_nick] = {"items": [ingredients[h][item] + '-' + h]}