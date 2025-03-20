from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove  # Добавленный импорт
from database import get_user_data, add_user
from keyboards import get_main_menu, end_session_keyboard, get_pomodoro_menu, get_back_to_main_menu
from states import UserState
from services import ask_openrouter
from config import PSYCHOLOGIST_PROMPT
import asyncio
import random
import logging

# Обработчик команды /start
async def send_welcome(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    if not user_data:
        await message.answer("Привет! Я твой помощник для психологической поддержки. Как тебя зовут?")
        await state.set_state(UserState.waiting_for_name)
    else:
        await message.answer(f"С возвращением, {user_data[1]}! Выбери действие:", reply_markup=get_main_menu())
        await state.set_state(UserState.in_session)

# Обработчик команды /menu
async def send_menu(message: types.Message):
    await message.answer("Выбери действие:", reply_markup=get_main_menu())

# Обработчик получения имени пользователя
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    user_id = message.from_user.id
    add_user(user_id, user_name)
    await state.update_data(user_name=user_name)
    await message.answer(f"Приятно познакомиться, {user_name}! Выбери действие:", reply_markup=get_main_menu())
    await state.set_state(UserState.in_session)

# Список сообщений о генерации
GENERATION_MESSAGES = [
    "✨ Ищу лучшие слова для вас. Пожалуйста, подождите.",
    "🌸 Elysia погружается в ваш запрос... Пожалуйста, наберитесь терпения..",
    "🌿 Ищу ответ в глубинах вашего запроса. Один момент...",
    "🌅 Elysia медитирует над вашим вопросом. Пожалуйста, подождите.",
    "💭 Формирую ответ...",
    "🌞 Elysia ищет светлые мысли для вас. Пожалуйста, подождите."
    "🌳 Elysia ищет ответ в глубинах леса. Пожалуйста, подождите."
    "🌊 Волны мыслей несут ваш ответ. Один момент..."
    "🍃 Elysia вдыхает вдохновение для вашего запроса. Пожалуйста, подождите."
]


# Функция для анимации загрузки
async def show_loading_animation(message: types.Message, status_message: types.Message):
    for _ in range(3):  # Повторяем анимацию 3 раза
        text = random.choice(GENERATION_MESSAGES)  # Выбираем случайное сообщение
        await status_message.edit_text(text)  # Редактируем сообщение
        await asyncio.sleep(1)  # Пауза между сообщениями

# Функция для анимации загрузки
async def show_loading_animation(message: types.Message, status_message: types.Message):
    for _ in range(3):  # Повторяем анимацию 3 раза
        text = random.choice(GENERATION_MESSAGES)  # Выбираем случайное сообщение
        await status_message.edit_text(text)  # Редактируем сообщение
        await asyncio.sleep(1)  # Пауза между сообщениями

# Обработчик кнопки "AI психолог"
async def start_psychologist(callback: types.CallbackQuery, state: FSMContext):
    # Отправляем описание функции
    await callback.message.answer(
        "🧠 **AI психолог**\n\n"
        "Ты можешь общаться с AI психологом. Он поможет тебе разобраться в твоих мыслях и чувствах.\n\n"
        "Напиши свой запрос, и я постараюсь помочь."
    )
    
    # Устанавливаем состояние "ожидание запроса"
    await state.set_state("waiting_for_query")
    await callback.answer()

# Обработчик запроса пользователя
async def handle_user_query(message: types.Message, state: FSMContext):
    # Получаем текущую историю сообщений
    user_data = await state.get_data()
    messages = user_data.get("messages", [])
    
    # Если история пуста, добавляем системный промт
    if not messages:
        messages.append({"role": "system", "content": PSYCHOLOGIST_PROMPT})
    
    # Добавляем запрос пользователя в историю
    messages.append({"role": "user", "content": message.text})
    
    # Сохраняем историю в состоянии
    await state.update_data(messages=messages)
    
    # Отправляем сообщение о состоянии
    status_message = await message.answer("🔄 Генерация ответа...")
    
    # Запускаем анимацию загрузки
    await show_loading_animation(message, status_message)
    
    # Отправляем запрос к OpenRouter
    try:
        response = ask_openrouter(messages)
        
        if len(response) > 4096:
            response = response[:4096]
        
        # Удаляем сообщение о состоянии и отправляем ответ как новое сообщение
        await status_message.delete()
        await message.answer(response)
        
        # Добавляем ответ нейросети в историю
        messages.append({"role": "assistant", "content": response})
        await state.update_data(messages=messages)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
        await status_message.edit_text("Извините, произошла ошибка при обработке вашего запроса.")
            
# Обработчик кнопки "Рефлексия"
async def handle_reflection(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📝 **Рефлексия**\n\n"
        "Эта функция пока в разработке. Следи за обновлениями!",
        reply_markup=get_back_to_main_menu()
    )
    await callback.answer()

# Обработчик кнопки "Журнал"
async def handle_journal(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📔 **Журнал**\n\n"
        "Эта функция пока в разработке. Следи за обновлениями!",
        reply_markup=get_back_to_main_menu()
    )
    await callback.answer()

# Обработчик кнопки "Профиль"
async def handle_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user_data(user_id)
    if user_data:
        await callback.message.edit_text(
            f"👤 **Профиль**\n\n"
            f"Имя: {user_data[1]}\n"
            f"Дней в боте: {user_data[2]}\n"
            f"Префронтальная кора: {user_data[3]}\n"
            f"Гиппокамп: {user_data[4]}\n"
            f"Миндалевидное тело: {user_data[5]}",
            reply_markup=get_back_to_main_menu()
        )
    else:
        await callback.message.edit_text("Вы еще не зарегистрированы. Напишите /start.", reply_markup=get_back_to_main_menu())
    await callback.answer()

# Обработчик кнопки "Pomodoro Tracker"
async def start_pomodoro_tracker(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🍅 **Pomodoro Tracker**\n\n"
        "Этот таймер поможет тебе сосредоточиться на задачах. "
        "Работай 25 минут, затем отдыхай 5 минут. Цикл повторяется, пока ты не решишь остановиться.",
        reply_markup=get_pomodoro_menu()
    )
    await callback.answer()

# Обработчик кнопки "Запустить таймер"
async def start_pomodoro_timer(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Таймер запущен! 🕒 25 минут фокуса.",
        reply_markup=get_pomodoro_menu(is_timer_running=True)
    )
    await callback.answer()
    
    # Запускаем цикл Pomodoro
    await pomodoro_cycle(callback.message, state)

# Обработчик кнопки "Остановить таймер"
async def stop_pomodoro_timer(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🍅 **Pomodoro Tracker**\n\n"
        "Этот таймер поможет тебе сосредоточиться на задачах. "
        "Работай 25 минут, затем отдыхай 5 минут. Цикл повторяется, пока ты не решишь остановиться.",
        reply_markup=get_pomodoro_menu()
    )
    await callback.answer()

# Обработчик кнопки "Главное меню"
async def return_to_main_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбери действие:", reply_markup=get_main_menu())
    await callback.answer()

# Функция для цикла Pomodoro
async def pomodoro_cycle(message: types.Message, state: FSMContext):
    while True:
        # 25 минут фокуса
        await asyncio.sleep(25 * 60)  # 25 минут в секундах
        await message.answer("🕒 25 минут прошли! Начинается 5-минутный перерыв.")
        
        # 5 минут перерыва
        await asyncio.sleep(5 * 60)  # 5 минут в секундах
        await message.answer("🕒 Перерыв закончился. Начинается новый цикл фокуса (25 минут).")

# Обработчик завершения сеанса
async def end_psychologist_session(message: types.Message, state: FSMContext):
    # Очищаем историю сообщений
    await state.update_data(messages=[])
    
    # Отправляем сообщение о завершении сеанса
    await message.answer(
        "Сеанс завершён. Если у тебя есть ещё вопросы, просто нажми кнопку «AI психолог».",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Возвращаем пользователя в главное меню
    await message.answer("Выбери действие:", reply_markup=get_main_menu())
    await state.set_state(None)
```
# Обработчик всех сообщений (для поддержания диалога)
async def handle_message(message: types.Message, state: FSMContext):
    if message.text.lower() == 'завершить сеанс':
        await end_psychologist_session(message, state)
    else:
        user_data = await state.get_data()
        messages = user_data.get("messages", [])
        messages.append({"role": "user", "content": message.text})
        response = ask_openrouter(messages)
        messages.append({"role": "assistant", "content": response})
        await state.update_data(messages=messages)
        try:
            if len(response) > 4096:
                response = response[:4096]
            await message.answer(response, reply_markup=end_session_keyboard)
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения: {e}")
