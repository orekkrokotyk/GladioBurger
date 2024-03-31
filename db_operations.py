from config import *
from main import main_menu


# Регистрация
def name(message):
    global r_name
    r_name = message.text
    msg = bot.send_message(message.chat.id, f"""Ник""")
    bot.register_next_step_handler(msg, nick)


def nick(message):
    global nickname
    nickname = message.text
    connection = sqlite3.connect('Users.db', check_same_thread=False)
    cursor = connection.cursor()
    g = cursor.execute(f"""SELECT nickname FROM Users""").fetchall()
    s = [g[i][0] for i in range(len(g))]
    if nickname in s:
        msg = bot.send_message(message.chat.id, f"""Ник уже занят""")
        bot.register_next_step_handler(msg, nick)
    else:
        msg = bot.send_message(message.chat.id, f"""Пороль""")
        bot.register_next_step_handler(msg, pas)


def pas(message):
    global password
    password = message.text
    markup = main_menu()
    bot.send_message(message.chat.id, f"""Ты зарегестрирован""", reply_markup=markup)
    u_id = message.from_user.id
    reg(str(u_id))


def reg(u_id):
        global invent
        invent["inventar"][nickname] = {"chests": [], "items": [],
                                        "burger": burger}
        connection = sqlite3.connect('Users.db', check_same_thread=False)
        cursor = connection.cursor()
        g = cursor.execute(f"""SELECT user_id FROM User_id_nick""").fetchall()
        s = [g[i][0] for i in range(len(g))]
        cursor.execute(
            f"""INSERT INTO Users (name, nickname, password) VALUES ('{r_name}', '{nickname}', '{password}')""")
        if u_id in s:
            cursor.execute(f"""UPDATE User_id_nick SET nick = '{nickname}' WHERE user_id = '{u_id}'""")
        else:
            cursor.execute(f"INSERT INTO User_id_nick (user_id, nick) VALUES ('{u_id}', '{nickname}')")
        connection.commit()
        connection.close()


# Вход в существующий аккаунт
def log_nick(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    global l_nick
    global n_pass
    l_nick = message.text
    connection = sqlite3.connect('Users.db', check_same_thread=False)
    cursor = connection.cursor()
    g = cursor.execute(f"""SELECT nickname FROM Users""").fetchall()
    s = [g[i][0] for i in range(len(g))]
    if l_nick not in s:
        size_but_1 = types.KeyboardButton("Вход")
        size_but_2 = types.KeyboardButton("Регестрация")
        markup.add(size_but_1)
        markup.add(size_but_2)
        bot.send_message(message.chat.id, "Такого никнейма нет. Войдите с другим или зарегестрируйте этот",
                         reply_markup=markup)
    else:
        n_pass = cursor.execute(
            f"""SELECT password FROM Users WHERE nickname is '{l_nick}'""").fetchall()
        connection.commit()
        n_pass = n_pass[0][0]
        msg = bot.send_message(message.chat.id, f"""Введите свой пароль""")
        bot.register_next_step_handler(msg, log_pass)
    connection.close()


def log_pass(message):
    global l_pas
    l_pas = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    connection = sqlite3.connect('Users.db', check_same_thread=False)
    cursor = connection.cursor()
    if l_pas == n_pass:
        cursor.execute(f"""UPDATE User_id_nick SET nick = '{l_nick}' WHERE user_id = '{message.from_user.id}'""")
        connection.commit()
        markup = main_menu()
        bot.send_message(message.chat.id, "Вы вошли в аккаунт", reply_markup=markup)
    else:
        size_but_1 = types.KeyboardButton("Вход")
        size_but_2 = types.KeyboardButton("Регестрация")
        markup.add(size_but_1)
        markup.add(size_but_2)
        bot.send_message(message.chat.id, "Не верный пароль, попробуйте ещё или зарегестрируйтесь", reply_markup=markup)


# Выход из аккаунта
def quit_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    connection = sqlite3.connect('Users.db', check_same_thread=False)
    cursor = connection.cursor()
    g = cursor.execute(f"""SELECT user_id FROM User_id_nick""").fetchall()
    s = [g[i][0] for i in range(len(g))]
    print(s)
    cursor.execute(
        f"""UPDATE User_id_nick SET nick = '{message.from_user.id}' WHERE user_id = '{message.from_user.id}'""")
    connection.commit()
    connection.close()
    size_but_1 = types.KeyboardButton("Вход")
    size_but_2 = types.KeyboardButton("Регестрация")
    markup.add(size_but_1)
    markup.add(size_but_2)
    bot.send_message(message.chat.id, f"""Вы вышли из своего аккаунта""", reply_markup=markup)


# Функция ищющая ник пользователя по telegram id
def search(u_id):
    global i_nick
    connection = sqlite3.connect('Users.db', check_same_thread=False)
    cursor = connection.cursor()
    i_nick = cursor.execute(
        f"""SELECT nick FROM User_id_nick WHERE user_id is '{u_id}'""").fetchall()
    connection.commit()
    print(i_nick)
    i_nick = i_nick[0][0]
    connection.close()
    return i_nick

