from config import *
from db_operations import search


def ingredient_numerator(ingrid, user_id):
    number = "2"
    if ingrid in burg[str(user_id)]["ingredients"].keys():
        try:
            print(ingrid[-1])
            print(int(ingrid[-1]))
            number = int(ingrid[-1]) + 1
            return ingredient_numerator(ingrid[:-2] + f" {number}", user_id)
        except:
            return ingredient_numerator(ingrid + f" {number}", user_id)
    else:
        return ingrid


# Дабовление в список игроков ожидающих бой
def wait_list(message):
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
                v_with_num = ingredient_numerator(v, str(users_id[i]))
                burg[str(users_id[i])]["ingredients"][v_with_num] = [ingredient[v]['hp'], ingredient[v]['hp']]
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
                try:
                    int(list_id[g][-1])
                    ingred = list_id[g][:-2]
                except:
                    ingred = list_id[g]
                e_t[id_fight] = "False"
                f = open("end_turn.json", 'w', encoding='utf8')
                json.dump(e_t, f, ensure_ascii=False)
                f.close()
                bot.send_message(int(id_1), f"Бургер атакует {ingred}-ой")
                if ingred == "Булука 🥖":
                    e_t[id_fight] = "True"
                    print(f)
                elif ingredient[ingred]['skill'][0] == damage:
                    ingredient[ingred]['skill'][0](str(id_fight), ingred,
                                                   ingredient[ingred]['skill'][1], id_1, id_2)
                elif ingredient[ingred]['skill'][0] != damage:
                    ingredient[ingred]['skill'][0](str(id_fight), ingredient[ingred]['skill'][1], id_1, id_2)
            # Проверка нужная для того что-бы бот не отправлял сообщение второму игроку до того как первый не выбрал ингридиент для взаимодействия
            while e_t[id_fight] == "False":
                useless += 0
            if g < len(list_id_2):
                try:
                    int(list_id_2[g][-1])
                    ingred = list_id_2[g][:-2]
                except:
                    ingred = list_id_2[g]
                e_t[id_fight] = "False"
                f = open("end_turn.json", 'w', encoding='utf8')
                json.dump(e_t, f, ensure_ascii=False)
                f.close()
                bot.send_message(int(id_2), f"Бургер атакует {ingred}-ой")
                if ingred == "Булука 🥖":
                    e_t[id_fight] = "True"
                elif ingredient[ingred]['skill'][0] == damage:
                    ingredient[ingred]['skill'][0](str(id_fight), ingred,
                                                         ingredient[ingred]['skill'][1], id_2, id_1)
                elif ingredient[ingred]['skill'][0] != damage:
                    ingredient[ingred]['skill'][0](str(id_fight), ingredient[ingred]['skill'][1], id_2,
                                                         id_1)
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

    del figh[id_fight]
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
    bot.send_message(int(id_1), "Вот куда вы можете куснуть аппанента", reply_markup=markup)
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
    if burg[str(id_2)]["color"] == 1:
        burg[id_2]["ingredients"][ingred_2][0] -= int(value)
        burg[str(id_2)]["color"] = 0
    if burg[str(id)]["god"] == 1:
        value = 0
    burg[id_2]["ingredients"][ingred_2][0] -= int(value)
    e_t[id_fight] = "True"
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
    bot.send_message(int(id_1), "Вот куда вы можете добавить здоровя", reply_markup=markup)
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
    bot.send_message(int(id_1), "Вот куда вы можете добавить защиты", reply_markup=markup)
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
    bot.send_message(int(id_1), "Вот куда вы можете добавить защиты", reply_markup=markup)
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
    bot.send_message(int(id_1), "Вот где вы можете высосать сок", reply_markup=markup)


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
    global burg
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    burg[str(id)]["color"] = 1
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()


def copy(id_fight, value, id_1, id_2):
    global burg
    markup = types.InlineKeyboardMarkup(row_width=1)
    g = 0
    for i in burg[id_1]["ingredients"]:
        g += 1
        btn = types.InlineKeyboardButton(text=f"{g}: {i}", callback_data=f"copy{i}")
        markup.add(btn)
    inf[id_1] = [id_2, id_fight]
    bot.send_message(int(id_1), "Вот чьи способности вы можете скопировать", reply_markup=markup)

def copy_play(id_1, ingred):
    global burg
    id_2 = inf[str(id_1)][0]
    id_fight = inf[str(id_1)][1]
    if ingredient[ingred]['skill'][0] == damage:
        ingredient[ingred]['skill'][0](str(id_fight), ingred, ingredient[ingred]['skill'][1], id_1, id_2)
    elif ingredient[ingred]['skill'][0] != damage:
        ingredient[ingred]['skill'][0](str(id_fight), ingredient[ingred]['skill'][1], id_1, id_2)
    e_t[id_fight] = "True"


def god(id_fight, ingred_1, value, id_1, id_2):
    global burg
    global inf
    global figh
    markup = types.InlineKeyboardMarkup(row_width=1)
    g = 0
    for i in burg[id_2]["ingredients"]:
        g += 1
        btn = types.InlineKeyboardButton(text=f"{g}: {i}", callback_data=f"place prov{i}")
        markup.add(btn)
    inf[id_1] = [id_2, ingred_1, value, id_fight]
    bot.send_message(int(id_1), "Вот кого вы можете справоцировать ", reply_markup=markup)
    f = open("trash.json", 'w', encoding='utf8')
    json.dump(inf, f, ensure_ascii=False)
    f.close()


def god_play(id_1, ingred_2):
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
    if burg[str(id_2)]["color"] == 1:
        burg[id_2]["ingredients"][ingred_2][0] -= int(value)
        burg[str(id_2)]["color"] = 0
    burg[id_2]["ingredients"][ingred_2][0] -= int(value)
    burg[str(id)]["god"] = 1
    e_t[id_fight] = "True"
    del inf[str(id_1)]
    f = open("trash.json", 'w', encoding='utf8')
    json.dump(inf, f, ensure_ascii=False)
    f.close()


ingredient = {
            'томат': {'hp': 10, 'skill': [heal, 5]}, 'салат': {'hp': 14, 'skill': [heal, 7]},
            'огурец': {'hp': 20, 'skill': [damage, 5]}, 'солёный_огурец': {'hp': 5, 'skill': [thorn, 5]},
            'морковь': {'hp': 14, 'skill': [damage, 7]}, 'чеснок': {'hp': 8, 'skill': [thorn, 8]},
            'капуста': {'hp': 20, 'skill': [heal, 10]}, 'картофель': {'hp': 10, 'skill': [damage, 5]},
            'репа': {'hp': 16, 'skill': [heal, 8]}, 'крапива': {'hp': 50, 'skill': [vampirism, 25]},
            'острый_перец': {'hp': 30, 'skill': [fire, 15]},
            "Котлета 🟤": {'hp': 50, 'skill': [damage, 1500]},
            "Булука 🥖": {'hp': 10000}, 'лук': {'hp': 50, 'skill': [thorn, 15]},
            'сыр': {'hp': 50, 'skill': [armor, 10]}, 'свёкла': {'hp': 50, 'skill': [coloring, 0]},
            'горох': {'hp': 50, 'skill': [copy, 0]}, 'сельдерей': {'hp': 50, 'skill': [damage, 15]},
            'баклажан': {'hp': 50, 'skill': [armor, 15]}, 'цветная_капуста': {'hp': 50, 'skill': [god, 5]},
            'пекинская_капуста': {'hp': 50, 'skill': [damage, 20]}, 'кабачок': {'hp': 50, 'skill': [god, 7]},
            'фасоль': {'hp': 50, 'skill': [coloring, 0]}, 'брюква': {'hp': 50, 'skill': [armor, 17]},
            'укроп': {'hp': 50, 'skill': [copy, 0]}, 'лук-порей': {'hp': 50, 'skill': [damage, 20]}
              }
