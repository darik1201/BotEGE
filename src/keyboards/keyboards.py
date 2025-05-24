from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
def get_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню бота"""
    keyboard = [
        [KeyboardButton(text="Ввести баллы"), KeyboardButton(text="Мои баллы")],
        [KeyboardButton(text="Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
def get_subjects_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с предметами ЕГЭ"""
    subjects = [
        "Русский язык", "Профильная математика", "Базовая математика",
        "Физика", "Химия", "История", "Обществознание", "Информатика",
        "Биология", "География", "Английский язык", "Немецкий язык",
        "Французский язык", "Испанский язык", "Китайский язык", "Литература"
    ]
    keyboard = []
    for i in range(0, len(subjects), 2):
        row = [InlineKeyboardButton(text=subjects[i], callback_data=f"subject_{subjects[i]}")]
        if i + 1 < len(subjects):
            row.append(InlineKeyboardButton(text=subjects[i + 1], callback_data=f"subject_{subjects[i + 1]}"))
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)