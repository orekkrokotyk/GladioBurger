from config import *
from db_operations import search


# Дабовление в список игроков ожидающих бой
def waiting_list(message):
    global gladiators
    gladiators.append(str(message.from_user.id))
    bot.send_message(message.chat.id, "Вы в списке гладиаторов ожидающих бой")
    print(gladiators)
    if len(gladiators) >= 2:
        war_l = [x for x in figh]
        figh[str(int(war_l[-1]) + 1)] = gladiators[:2]
        del gladiators[:2]

        prep_fight(str(int(war_l[-1]) + 1))


# подготовка к бою
def prep_fight(id_fight):
    global figh
    users_id = figh[id_fight]
    for i in range(len(users_id)):
        bot.send_message(users_id[i], f"Ваш враг - {search(users_id[i - 1])}")
        # создание словаря с ингридиентами соперников и их характеристиками
        burg[str(users_id[i])] = {"ingredients": {}, "thorns": 0}
        for v in (invent["inventar"][search(users_id[i])]["burger"]):
            if v != '':
                burg[str(users_id[i])]["ingredients"][v] = [ingredient[v]['hp'], ingredient[v]['hp']]
    fight(id_fight)


# Модуль боя
def fight(id_fight):
    useless = 0
    t = []
    z = []
    global figh
    global e_t
    print(figh)
    id_1 = figh[id_fight][0]
    id_2 = figh[id_fight][1]
    f = open("burger_data.json", 'r+', encoding="utf-8")
    burg = json.load(f)
    f.close()
    # бой продолжается до момента существования котлеты в бургере
    while 'Котлета 🟤' in list(burg[str(id_1)]["ingredients"]) and "Котлета 🟤" in list(burg[str(id_2)]["ingredients"]):
        f = open("burger_data.json", 'r+', encoding="utf-8")
        burg = json.load(f)
        f.close()
        list_id = list(burg[str(id_1)]["ingredients"])
        list_id_2 = list(burg[str(id_2)]["ingredients"])
        max_len = [len(list_id), len(list_id_2)]
        for g in range(0, max(max_len)):
            if g < len(list_id):
                e_t[id_fight] = "False"
                f = open("end_turn.json", 'w', encoding='utf8')
                json.dump(e_t, f, ensure_ascii=False)
                f.close()
                bot.send_message(int(id_1), f"{list_id[g]} атакует ")
                if list_id[g] == "Булука 🥖":
                    e_t[id_fight] = "True"
                    print(f)
                elif ingredient[list_id[g]]['skill'][0] == damage:
                    ingredient[list_id[g]]['skill'][0](str(id_fight), list_id[g],
                                                       ingredient[list_id[g]]['skill'][1], id_1, id_2)
                elif ingredient[list_id[g]]['skill'][0] != damage:
                    ingredient[list_id[g]]['skill'][0](str(id_fight), ingredient[list_id[g]]['skill'][1], id_1, id_2)
            # Проверка нужная для того что-бы бот не отправлял сообщение второму игроку до того как первый не выбрал ингридиент для взаимодействия
            while e_t[id_fight] == "False":
                useless += 0
            if g < len(list_id_2):
                e_t[id_fight] = "False"
                f = open("end_turn.json", 'w', encoding='utf8')
                json.dump(e_t, f, ensure_ascii=False)
                f.close()
                bot.send_message(int(id_2), f"Бургер атакует {list_id_2[g]}-ой")
                if list_id_2[g] == "Булука 🥖":
                    e_t[id_fight] = "True"
                elif ingredient[list_id_2[g]]['skill'][0] == damage:
                    ingredient[list_id_2[g]]['skill'][0](str(id_fight), list_id_2[g],
                                                       ingredient[list_id_2[g]]['skill'][1], id_2, id_1)
                elif ingredient[list_id_2[g]]['skill'][0] != damage:
                    ingredient[list_id_2[g]]['skill'][0](str(id_fight), ingredient[list_id_2[g]]['skill'][1], id_2, id_1)
            while e_t[id_fight] == "False":
                useless += 0
        f = open("burger_data.json", 'r+', encoding="utf-8")
        burg = json.load(f)
        f.close()
        # Поиск умерщих ингридиентов
        for x, y in burg[str(id_1)]["ingredients"].items():
            if y[0] <= 0:
                z.append(x)
        for x, y in burg[str(id_2)]["ingredients"].items():
            if y[0] <= 0:
                t.append(x)
        # Удаление умерших ингридиентов
        for i in t:
            del burg[str(id_2)]["ingredients"][i]
        for i in z:
            del burg[str(id_1)]["ingredients"][i]
        # Определение победителя
        if 'котлета' not in list(burg[str(id_1)]["ingredients"]):
            bot.send_message(int(id_1), f"Победил игрок {id_2}")
            bot.send_message(int(id_2), f"Победил игрок {id_2}")
            return
        elif 'котлета' not in list(burg[str(id_2)]["ingredients"]):
            bot.send_message(int(id_1), f"Победил игрок {id_1}")
            bot.send_message(int(id_2), f"Победил игрок {id_1}")
            return
        else:
            bot.send_message(int(id_1), f"Следующий круг")
            bot.send_message(int(id_2), f"Следующий круг")

        t = []
        z = []

    del fight[id_fight]
    del burg[str(id_1)]
    del burg[str(id_2)]

    pass


# Функции взаимодействия
def damage(id_fight, ingred_1, value, id_1, id_2):
    global burg
    global inf
    global figh
    markup = types.InlineKeyboardMarkup(row_width=1)
    g = 0
    for i in burg[id_2]["ingredients"]:
        g += 1
        btn = types.InlineKeyboardButton(text=f"{g}: {i}", callback_data=f"place attack{i}")
        markup.add(btn)
    inf[id_1] = [id_2, ingred_1, value, id_fight]
    bot.send_message(int(id_1), "Вот куда вы можите куснуть аппанента", reply_markup=markup)
    f = open("trash.json", 'w', encoding='utf8')
    json.dump(inf, f, ensure_ascii=False)
    f.close()


def damage_play(id_1, ingred_2):
    global burg
    global inf
    global e_t
    id_2 = inf[str(id_1)][0]
    ingred_1 = inf[str(id_1)][1]
    value = inf[str(id_1)][2]
    id_fight = inf[str(id_1)][3]
    if burg[id_2]["thorns"] != 0:
        burg[id_1]["ingredients"][ingred_1][0] -= burg[id_2]["thorns"]
        burg[id_2]["thorns"] = 0
    burg[id_2]["ingredients"][ingred_2][0] -= int(value)
    e_t[id_fight ] = "True"
    del inf[str(id_1)]
    f = open("trash.json", 'w', encoding='utf8')
    json.dump(inf, f, ensure_ascii=False)
    f.close()



def heal(id_fight, value, id_1, id_2):
    global burg
    global inf
    markup = types.InlineKeyboardMarkup(row_width=1)
    g = 0
    for i in burg[id_1]["ingredients"]:
        g += 1
        btn = types.InlineKeyboardButton(text=f"{g}: {i}", callback_data=f"place heal{i}")
        markup.add(btn)
    inf[id_1] = [id_2, value, id_fight]
    bot.send_message(int(id_1), "Вот куда вы можите добавить здоровя", reply_markup=markup)
    f = open("trash.json", 'w', encoding='utf8')
    json.dump(inf, f, ensure_ascii=False)
    f.close()


def heal_play(id_1, ingred):
    global burg
    global e_t
    print(inf[str(id_1)])
    value = inf[str(id_1)][1]
    id_fight = inf[str(id_1)][2]
    if burg[str(id_1)]["ingredients"][ingred][0] + int(value) >= burg[str(id_1)]["ingredients"][ingred][1]:
        burg[str(id_1)]["ingredients"][ingred][0] = burg[str(id_1)]["ingredients"][ingred][1]
    else:
        burg[str(id_1)]["ingredients"][ingred][0] += int(value)
    print(e_t[id_fight], 5)
    e_t[id_fight] = "True"
    print(e_t[id_fight], 6)


def thorn(id_fight, value, id_1, id_2):
    global burg
    global figh
    global e_t
    bot.send_message(int(id_1), "Ваш бургер зашипован")
    burg[str(id_1)]["thorns"] += int(value)
    e_t[id_fight] = "True"


def armor(id_fight, value, id_1, id_2):
    global burg
    markup = types.InlineKeyboardMarkup(row_width=1)
    g = 0
    for i in burg[id_1]["ingredients"]:
        g += 1
        btn = types.InlineKeyboardButton(text=f"{g}: {i}", callback_data=f"place armor{i}")
        markup.add(btn)
    inf[id_1] = [id_2, value, id_fight]
    bot.send_message(int(id_1), "Вот куда вы можите добавить защиты", reply_markup=markup)
    f = open("trash.json", 'w', encoding='utf8')
    json.dump(inf, f, ensure_ascii=False)
    f.close()


def armor_play(id_1, ingred):
    global burg
    global e_t
    print(inf[str(id_1)])
    value = inf[str(id_1)][1]
    id_fight = inf[str(id_1)][2]
    burg[str(id_1)]["ingredients"][ingred][1] += int(value)
    burg[str(id_1)]["ingredients"][ingred][0] += int(value)
    print(e_t[id_fight], 5)
    e_t[id_fight] = "True"
    print(e_t[id_fight], 6)


def fire(id_fight, value, id_1, id_2):
    global burg
    markup = types.InlineKeyboardMarkup(row_width=1)
    g = 0
    for i in burg[id_1]["ingredients"]:
        g += 1
        btn = types.InlineKeyboardButton(text=f"{g}: {i}", callback_data=f"place fire{i}")
        markup.add(btn)
    inf[id_1] = [id_2, value, id_fight]
    bot.send_message(int(id_1), "Вот куда вы можите добавить защиты", reply_markup=markup)
    f = open("trash.json", 'w', encoding='utf8')
    json.dump(inf, f, ensure_ascii=False)
    f.close()


def fire_play(id_1, ingred):
    global burg
    global e_t
    m = []
    id_2 = inf[str(id_1)][0]
    value = inf[str(id_1)][1]
    id_fight = inf[str(id_1)][2]
    for i in burg[str(id_2)]["ingredients"]:
        m.append(i)
    burg[str(id_2)]["ingredients"][ingred][0] -= int(value)
    if m.index(ingred) >= 1:
        burg[str(id_2)]["ingredients"][m[m.index(ingred) - 1]][0] -= int(value) // 2
    if m.index(ingred) <= len(m) - 2:
        burg[str(id_2)]["ingredients"][m[m.index(ingred) + 1]][0] -= int(value) // 2
    print(e_t[id_fight], 5)
    e_t[id_fight] = "True"
    print(e_t[id_fight], 6)


def vampirism(id_fight, value, id_1, id_2):
    global burg
    markup = types.InlineKeyboardMarkup(row_width=1)
    g = 0
    for i in burg[id_1]["ingredients"]:
        g += 1
        btn = types.InlineKeyboardButton(text=f"{g}: {i}", callback_data=f"place fire{i}")
        markup.add(btn)
    inf[id_1] = [id_2, value, id_fight]
    bot.send_message(int(id_1), "Вот где вы можите высосать сок", reply_markup=markup)


def vampirism_play(id_1, ingred):
    global burg
    id_2 = inf[str(id_1)][0]
    value = inf[str(id_1)][1]
    id_fight = inf[str(id_1)][2]
    burg[str(id_2)]["ingredients"][ingred][0] -= int(value)
    burg[str(id_1)]["ingredients"]['крапива'][0] += int(value)
    burg[str(id_1)]["ingredients"]['крапива'][1] += int(value)
    print(e_t[id_fight], 5)
    e_t[id_fight] = "True"
    print(e_t[id_fight], 6)

def coloring(id, value):
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    burg[str(id)]["color"] = 1
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()



ingredient = {'томат': {'hp': 10, 'skill': [heal, 5]}, 'салат': {'hp': 14, 'skill': [heal, 7]},
              'огурец': {'hp': 20, 'skill': [damage, 5]}, 'солёный_огурец': {'hp': 5, 'skill': [thorn, 5]},
              'морковь': {'hp': 14, 'skill': [damage, 7]}, 'чеснок': {'hp': 8, 'skill': [thorn, 8]},
              'капуста': {'hp': 20, 'skill': [heal, 10]}, 'картофель': {'hp': 10, 'skill': [damage, 5]},
              'репа': {'hp': 16, 'skill': [heal, 8]}, 'крапива': {'hp': 50, 'skill': [vampirism, 25]},
              'острый_перец': {'hp': 30, 'skill': [fire, 15]},
              "Котлета 🟤": {'hp': 50, 'skill': [damage, 1500]}}
