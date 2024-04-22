from config import *
from main import main_menu
from db_operations import search


def get_chest(message):
    global invent
    i_nick = search(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('common 120')
    btn2 = types.KeyboardButton('rare 210')
    btn3 = types.KeyboardButton('epic 360')
    btn4 = types.KeyboardButton('legendary 630')
    btn6 = types.KeyboardButton('Главное меню')
    markup.add(btn1, btn2, btn3, btn4)
    markup.add(btn6)
    bot.send_message(message.chat.id, 'Какой кейс вы хотите купить?', reply_markup=markup)
    print(invent['inventar'][i_nick])
    bot.send_message(message.chat.id, f"У вас {invent['inventar'][i_nick]['many']} минет")



def open_chest(callback):
    global invent
    i_nick = search(callback.message.chat.id)
    p = (invent["inventar"][i_nick]["chests"]).index(callback.data)
    del invent["inventar"][i_nick]["chests"][p]
    rarity = callback.data[:-7]
    chat_id = callback.message.chat.id
    markup = main_menu()
    for i in range(0, 5):
        for t in range(chests[rarity][i]):
            cr.append(list(ingredients.keys())[i])
    random.shuffle(cr)
    h = cr[random.randint(0, 100)]
    item = random.randint(0, len(ingredients[h]) - 1)
    bot.send_message(chat_id, h + ':', reply_markup=markup)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text=f"Описание", callback_data=f"description{ingredients[h][item]}"))
    bot.send_message(chat_id, ingredients[h][item], reply_markup=markup)
    cr.clear()

    if i_nick in invent["inventar"]:
        invent["inventar"][i_nick]["items"].append(ingredients[h][item] + '-' + h)
    else:
        invent["inventar"][i_nick] = {"items": [ingredients[h][item] + '-' + h]}



