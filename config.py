import json
import random
import sqlite3
import atexit

import telebot
from telebot import types


# TOKEN бота
token = '6394824094:AAHeEnAmzJOmVSBgLxPT2YXEP_qdqpFwZDk'
bot = telebot.TeleBot(token)


r_name = ""
nickname = ""
password = ""
l_nick = ""
l_pas = ""
n_pass = ""
i_nick = ""
burger = ["Булка 🥖", "", "", "", "Котлета 🟤", "", "", "Булка 🥖"]
clean_burger = ["Булка 🥖", "", "", "", "", "", "", "Булка 🥖"]
burger_update = ['1 place', '2 place', '3 place', '4 place', '5 place', '6 place', '7 place', '8 place']
burger_attack = ['1 place  attack', '2 place attack', '3 place attack', '4 place attack', '5 place attack',
                 '6 place attack', '7 place attack', '8 place attack']
add_cutlet = ['1 place_k', '2 place_k', '3 place_k', '4 place_k', '5 place_k', '6 place_k', '7 place_k', '8 place_k']


chests = {
    'common': [85, 15, 0, 0, 0],
    'rare': [50, 45, 5, 0, 0],
    'epic': [20, 48, 30, 2, 0],
    'legendary': [10, 20, 40, 29, 1],
    'mythical': [0, 0, 0, 0, 1]
}

ingredients = {
    'common': ["томат", "салат", "огурец", "солёный_огурец", "морковь", "чеснок", "репа", "капуста", "картофель"],
    'rare': ["лук", "сыр", "свёкла", "горох", "сельдерей", "баклажан", "цветная_капуста", "пекинская_капуста",
             "кабачок", "фасоль", "брюква", "укроп", "лук_порей"],
    'epic': ["тыква", "архис", "руккола", "брокколи", "редис", "петрушка", "корнишон"],
    'legendary': ["авокадо", "брюсельская капуста", "патиссон", "мангольд", "острый_перец"],
    'mythical': ["крапива"]
}

all_i = ['томат-common', 'салат-common', 'огурец-common', 'солёный_огурец-common', 'морковь-common', 'чеснок-common',
         'репа-common', 'капуста-common', 'картофель-common', 'лук-rare', 'сыр-rare', 'свёкла-rare', 'горох-rare',
         'сельдерей-rare', 'баклажан-rare', 'цветная_капуста-rare', 'пекинская_капуста-rare', 'кабачок-rare',
         'фасоль-rare',
         'брюква-rare', 'укроп-rare', 'лук_порей-rare', 'тыква-epic', 'арахис-epic', 'руккола-epic', 'брокколи-epic',
         'редис-epic', 'петрушка-epic', 'корнишон-epic', 'острый_перец-legendary', 'авокадо-legendary',
         'брюсельская капуста-legendary', 'патиссон-legendary', 'мангольд-legendary', 'крапива-mythical']

market = {"common": 120,
          "rare": 210,
          "epic": 360,
          "legendary": 630}


gladiators = []
cr = []
h = 0
n_war = 1

f = open("fight_data.json", 'r+', encoding="utf-8")
figh = json.load(f)
f.close()
f = open("burger_data.json", 'r+', encoding="utf-8")
burg = json.load(f)
f.close()
f = open("invent_data.json", 'r+', encoding="utf-8")
invent = json.load(f)
f.close()
f = open("trash.json", 'r+', encoding="utf-8")
inf = json.load(f)
f.close()
f = open("end_turn.json", 'r+', encoding="utf=8")
e_t = json.load(f)
f.close()
f = open("ingredient_property.json", "r+", encoding="utf-8")
ingredient_property = json.load(f)
f.close()


