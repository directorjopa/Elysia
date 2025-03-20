from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню
def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="AI психолог", callback_data="ai_psychologist")],
        [InlineKeyboardButton(text="Рефлексия", callback_data="reflection")],
        [InlineKeyboardButton(text="Журнал", callback_data="journal")],
        [InlineKeyboardButton(text="Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="Pomodoro Tracker", callback_data="pomodoro_tracker")],
    ])

# Клавиатура для завершения сеанса с нейросетью
end_session_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Завершить сеанс')]
    ],
    resize_keyboard=True
)

# Меню Pomodoro Tracker
def get_pomodoro_menu(is_timer_running=False):
    if is_timer_running:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Остановить таймер", callback_data="stop_pomodoro")],
            [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Запустить таймер", callback_data="start_pomodoro")],
            [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
        ])

# Кнопка "Главное меню" для ответов
def get_back_to_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ])
