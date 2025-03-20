import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import API_TOKEN
from handlers import (
    send_welcome, process_name, start_psychologist, end_psychologist_session,
    handle_reflection, handle_journal, handle_profile, start_pomodoro_tracker,
    start_pomodoro_timer, stop_pomodoro_timer, return_to_main_menu, handle_message,
    send_menu  # Добавляем новый обработчик
)
from database import init_db
from states import UserState

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)

# Регистрация обработчиков
def register_handlers(dp: Dispatcher):
    dp.message.register(send_welcome, Command("start"))
    dp.message.register(process_name, UserState.waiting_for_name)
    dp.message.register(send_menu, Command("menu"))  # Регистрируем команду /menu
    dp.callback_query.register(start_psychologist, lambda c: c.data == "ai_psychologist")
    dp.callback_query.register(handle_reflection, lambda c: c.data == "reflection")
    dp.callback_query.register(handle_journal, lambda c: c.data == "journal")
    dp.callback_query.register(handle_profile, lambda c: c.data == "profile")
    dp.callback_query.register(start_pomodoro_tracker, lambda c: c.data == "pomodoro_tracker")
    dp.callback_query.register(start_pomodoro_timer, lambda c: c.data == "start_pomodoro")
    dp.callback_query.register(stop_pomodoro_timer, lambda c: c.data == "stop_pomodoro")
    dp.callback_query.register(return_to_main_menu, lambda c: c.data == "main_menu")
    dp.message.register(end_psychologist_session, lambda message: message.text.lower() == 'завершить сеанс', UserState.in_session)
    dp.message.register(handle_message, UserState.in_session)

# Запуск бота
async def main():
    init_db()
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
