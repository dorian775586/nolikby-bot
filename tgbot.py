import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Вставьте сюда токен вашего бота
API_TOKEN = "8260030545:AAG9hcUJyuyec6cORIETBwJIR2Yl3aRrIGo"

# Замените этот URL на URL вашего фронтенда, когда вы его задеплоите на Render.
# Например: https://skidkifront.onrender.com
FRONTEND_URL = "https://skidkifrontend.onrender.com"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создаём специальную кнопку для веб-приложения
web_app_button = KeyboardButton(
    text="📚 Каталог", 
    web_app=WebAppInfo(url=FRONTEND_URL)
)

# Клавиатура с одной кнопкой "Каталог"
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [web_app_button],
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Это бот nolikby 🎉", reply_markup=main_kb)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
