from config import *
from main import main_menu


# Регистрация
def pas(message, nick):
    password = message.text
    markup = main_menu()
    bot.send_message(message.chat.id, f"""Ты зарегестрирован""", reply_markup=markup)
    u_id = message.from_user.id
    reg(str(u_id), nick, password)


def reg(u_id, nickname, password):
        global invent
        invent["inventar"][nickname] = {"chests": [], "items": [],
                                        "burger": burger}
        connection = sqlite3.connect('Users.db', check_same_thread=False)
        cursor = connection.cursor()
        g = cursor.execute(f"""SELECT user_id FROM User_id_nick""").fetchall()
        s = [g[i][0] for i in range(len(g))]
        cursor.execute(
            f"""INSERT INTO Users (nickname, password) VALUES ('{nickname}', '{password}')""")
        if u_id in s:
            cursor.execute(f"""UPDATE User_id_nick SET nick = '{nickname}' WHERE user_id = '{u_id}'""")
        else:
            cursor.execute(f"INSERT INTO User_id_nick (user_id, nick) VALUES ('{u_id}', '{nickname}')")
        connection.commit()
        connection.close()


# Вход в существующий аккаунт
def log_pass(message, nick):
    global l_pas
    l_pas = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    connection = sqlite3.connect('Users.db', check_same_thread=False)
    cursor = connection.cursor()
    if l_pas == n_pass:
        cursor.execute(f"""UPDATE User_id_nick SET nick = '{nick}' WHERE user_id = '{message.from_user.id}'""")
        connection.commit()
        markup = main_menu()
        bot.send_message(message.chat.id, "Вы вошли в аккаунт", reply_markup=markup)
    else:
        size_but_1 = types.KeyboardButton("Другой ник")

        markup.add(size_but_1)
        bot.send_message(message.chat.id, "Не верный пароль, попробуйте ещё раз", reply_markup=markup)


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


def search_nickname(message):
    connection = sqlite3.connect('Users.db', check_same_thread=False)
    cursor = connection.cursor()
    find_id = cursor.execute(
        f"""SELECT id FROM Users WHERE nickname is '{message.text}'""").fetchall()
    return find_id


