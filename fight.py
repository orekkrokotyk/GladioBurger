import json
import random
from random import randint
i = 0


def run(id):
    f = open("fight_data.txt", 'r+')
    fight = json.load(f)
    f.close()
    for c in fight:
        if id in fight[c]:
            n_fight = c
            if fight[n_fight].index(id) == 0:
                id_2 = fight[n_fight][1]
            elif fight[n_fight].index(id) == 1:
                id_2 = fight[n_fight][0]
    return[id_2, n_fight]

def tablo(id, id_2):
    global i
    i += 1
    f = open("fight_data.txt", 'r+')
    fight = json.load(f)
    f.close()
    fight[str(i)] = [id, id_2]
    f = open("fight_data.txt", 'w', encoding='utf8')
    json.dump(fight, f, ensure_ascii=False)
    f.close()
    print(fight)

def damage(id_1, id_2, ingred_1, value):
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    for i in
    if burg[str(id)]["prov"] = 1:
    ingred_2 = input(f'Введите второй ингредиент для дамага {id_1}: ')
    if burg[str(id_2)]["thorns"] != 0:
        burg[str(id_1)]["ingredients"][ingred_1][0] -= burg[str(id_2)]["thorns"]
        burg[str(id_2)]["thorns"] = 0
    burg[str(id_2)]["ingredients"][ingred_2][0] -= int(value)
    if burg[str(id_2)]["color"] == 2:
        burg[str(id_2)]["color"] = 0
        burg[str(id_2)]["ingredients"][ingred_2][0] -= int(value)
    if burg[str(id_2)]["color"] == 1:
        burg[str(id_1)]["color"] = 2
    burg[str(id_2)]["ingredients"][ingred_2][0] -= int(value)
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()

def heal(id, value):
    ingred = input(f'Второй ингредиент для отхила {id}: ')
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    if burg[str(id)]["ingredients"][ingred][0] + int(value) >= burg[str(id)]["ingredients"][ingred][1]:
        burg[str(id)]["ingredients"][ingred][0] = burg[str(id)]["ingredients"][ingred][1]
    else:
        burg[str(id)]["ingredients"][ingred][0] += int(value)
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()

def thorn(id, value):
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    burg[str(id)]["thorns"] += int(value)
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()

def armor(id, value):
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    ingred = input(f'Второй ингредиент для армор {id}: ')
    burg[str(id)]["ingredients"][ingred][1] += int(value)
    burg[str(id)]["ingredients"][ingred][0] += int(value)
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()

def fire(id, value):
    id_2 = run(id)[0]
    m = []
    ingred = input(f'Введите второй ингредиент для дамага {id}: ')
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    for i in burg[str(id_2)]["ingredients"]:
        m.append(i)
    burg[str(id_2)]["ingredients"][ingred][0] -= int(value)
    if m.index(ingred) >= 1:
        burg[str(id_2)]["ingredients"][m[m.index(ingred) - 1]][0] -= int(value) // 2
    if m.index(ingred) <= len(m) - 2:
        burg[str(id_2)]["ingredients"][m[m.index(ingred) + 1]][0] -= int(value) // 2
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()

def vampirism(id, value):
    ingred = input(f'Введите второй ингредиент для дамага {id}: ')
    id_2 = run(id)[0]
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    burg[str(id_2)]["ingredients"][ingred][0] -= int(value)
    burg[str(id)]["ingredients"]['крапива'][0] += int(value)
    burg[str(id)]["ingredients"]['крапива'][1] += int(value)
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()

def coloring(id, value):
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    burg[str(id)]["color"] = 1
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()

def clean(id, value):
    id_2 = run(id)[0]
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    for i in burg[str(id)]['ingredients']:
        burg[str(id)]['ingredients'][i][1] -= int(value)
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()

def copy(id, value):
    c = []
    for x,y in ingredient.items():
        c.append(x)
    h = (c[random.randint(0, len(c - 1))])
    ingredient[h[g]]['skill'][0](id, ingredient[h[g]]['skill'][1])

def prov(id, value):
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    burg[str(id)]["prov"] = 1
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()


ingredient = {'томат': {'hp': 10, 'skill': [heal, 5]},
              'салат': {'hp': 14, 'skill': [heal, 7]},
              'огурец': {'hp': 20, 'skill': [damage, 10]},
              'солёный_огурец': {'hp': 5, 'skill': [thorn, 5]},
              'морковь': {'hp': 14, 'skill': [damage, 7]},
              'чеснок': {'hp': 8, 'skill': [thorn, 8]},
              'капуста': {'hp': 20, 'skill': [heal, 10]},
              'картофель': {'hp': 10, 'skill': [damage, 5]},
              'репа': {'hp': 16, 'skill': [heal, 8]},
              'крапива': {'hp': 50, 'skill': [vampirism, 25]},
              'острый_перец': {'hp': 30, 'skill': [fire, 15]},
              'котлета': {'hp': 50, 'skill': [damage, 150]}
              }

def start(id, ingredients):
    f = open("burger_data.txt", 'r+')
    burg = json.load(f)
    f.close()
    burg[str(id)] = {}
    burg[str(id)]["ingredients"] = {}
    burg[str(id)]["thorns"] = 0
    for v in ingredients:
        burg[str(id)]["ingredients"][v] = [ingredient[v]['hp'], ingredient[v]['hp']]
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()

def fight(id):
    t = []
    z = []
    id_2 = run(id)[0]
    n_fight = run(id)[1]
    f = open("burger_data.txt", 'r+', encoding="utf-8")
    burg = json.load(f)
    f.close()
    while 'котлета' in list(burg[str(id)]["ingredients"]) and 'котлета' in list(burg[str(id_2)]["ingredients"]):
        f = open("burger_data.txt", 'r+', encoding="utf-8")
        burg = json.load(f)
        f.close()
        list_id = list(burg[str(id)]["ingredients"])
        list_id_2 = list(burg[str(id_2)]["ingredients"])
        max_len = [len(list_id), len(list_id_2)]
        for g in range(0, max(max_len)):
            if g < len(list_id):
                if ingredient[list_id[g]]['skill'][0] == damage:
                    ingredient[list_id[g]]['skill'][0](id, id_2, list_id[g], ingredient[list_id[g]]['skill'][1])
                elif ingredient[list_id[g]]['skill'][0] != damage:
                    ingredient[list_id[g]]['skill'][0](id, ingredient[list_id[g]]['skill'][1])
            if g < len(list_id_2):
                if ingredient[list_id_2[g]]['skill'][0] == damage:
                    ingredient[list_id_2[g]]['skill'][0](id_2, id, list_id_2[g], ingredient[list_id_2[g]]['skill'][1])
                elif ingredient[list_id_2[g]]['skill'][0] != damage:
                    ingredient[list_id_2[g]]['skill'][0](id_2, ingredient[list_id_2[g]]['skill'][1])
        f = open("burger_data.txt", 'r+', encoding="utf-8")
        burg = json.load(f)
        f.close()
        for x, y in burg[str(id)]["ingredients"].items():
            if y[0] <= 0:
                z.append(x)
        for x, y in burg[str(id_2)]["ingredients"].items():
            if y[0] <= 0:
                t.append(x)
        for i in t:
            del burg[str(id_2)]["ingredients"][i]
        for i in z:
            del burg[str(id)]["ingredients"][i]
        if 'котлета' not in list(burg[str(id)]["ingredients"]):
            print(f'победитель: {id_2}')
        elif 'котлета' not in list(burg[str(id_2)]["ingredients"]):
            print(f'победитель: {id}')
        t = []
        z = []
        f = open("burger_data.txt", 'w', encoding='utf8')
        json.dump(burg, f, ensure_ascii=False)
        f.close()
    f = open("fight_data.txt", 'r+', encoding="utf-8")
    fight = json.load(f)
    f.close()
    del fight[str(n_fight)]
    del burg[str(id)]
    del burg[str(id_2)]
    f = open("fight_data.txt", 'w', encoding='utf8')
    json.dump(fight, f, ensure_ascii=False)
    f.close()
    f = open("burger_data.txt", 'w', encoding='utf8')
    json.dump(burg, f, ensure_ascii=False)
    f.close()
