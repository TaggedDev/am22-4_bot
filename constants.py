from subject import Subject
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

SUBJECTS_LIST = {
    'Дискретка':    Subject('Дискретная Математика', 'math/discrete/', 'png'), 
    'Лин. Ал':      Subject('Линейная Алгебра', 'math/linear', 'pdf'), 
    'Мат. Анализ':  Subject('Математический Анализ', 'math/analys', 'png')
}

CANCEL_KEYBOARD = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('Назад')]], resize_keyboard=True, selective=True)

SUBJECTS_KEYBOARD = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton("Дискретка"), KeyboardButton("Мат. Анализ"), KeyboardButton("Лин. Ал")]],
    resize_keyboard=True, selective=True)