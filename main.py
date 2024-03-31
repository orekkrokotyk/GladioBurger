from config import *

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    size_but_1 = types.KeyboardButton("Кейсы")
    size_but_2 = types.KeyboardButton("Инвентарь")
    size_but_3 = types.KeyboardButton("Мой бургер")
    size_but_4 = types.KeyboardButton("В Бой!")
    markup.add(size_but_1, size_but_2, size_but_3)
    markup.add(size_but_4)
    return markup