import os
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
# Используем переменную окружения для токена
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")
    
# URL вашего фронтенда
FRONTEND_URL = os.getenv("FRONTEND_URL")
if not FRONTEND_URL:
    raise ValueError("FRONTEND_URL is not set in environment variables")
    
# URL вашего бэкенда
BACKEND_URL = os.getenv("BACKEND_URL")
if not BACKEND_URL:
    raise ValueError("BACKEND_URL is not set in environment variables")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет! Я бот магазина. Выберите опцию:",
                         reply_markup=main_keyboard())

# Клавиатура с основными кнопками
def main_keyboard():
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="🛒 Перейти в магазин", web_app=types.WebAppInfo(url=FRONTEND_URL))],
        ]
    )
    return keyboard

# Команда для получения списка всех предложений
@dp.message(Command("offers"))
async def cmd_offers(message: types.Message):
    try:
        response = requests.get(f"{BACKEND_URL}/offers")
        response.raise_for_status()
        offers = response.json()
        
        if not offers:
            await message.answer("Извините, сейчас нет доступных предложений.")
            return

        text = "Доступные предложения:\n\n"
        for offer in offers:
            text += f"**{offer['title']}**\n"
            text += f"Категория: {offer['category']}\n"
            text += f"Город: {offer['city']}\n"
            text += f"Скидка: {offer['discount']}%\n"
            text += f"Цена: {offer['price']} руб.\n"
            text += f"Популярность: {offer['popularity']}\n"
            text += f"Действует до: {offer['end_date']}\n"
            text += "-"*20 + "\n"
        
        await message.answer(text, parse_mode="Markdown")

    except requests.exceptions.RequestException as e:
        await message.answer(f"Произошла ошибка при получении предложений: {e}")
