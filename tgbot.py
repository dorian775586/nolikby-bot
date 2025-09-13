import asyncio
import os
import logging
import requests
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

load_dotenv()

# Замените токен на BOT_TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")

# Получите URL бэкенда из переменных окружения
BACKEND_URL = os.getenv("BACKEND_URL")
if not BACKEND_URL:
    raise ValueError("BACKEND_URL is not set in environment variables")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Включение логирования
logging.basicConfig(level=logging.INFO)

async def start_polling():
    await dp.start_polling(bot)

@dp.message()
async def handle_message(message: types.Message):
    logging.info(f"Received message: {message.text}")
    
    # Запрос к бэкенду для получения URL веб-приложения
    try:
        response = requests.get(f"{BACKEND_URL}/webapp_url")
        response.raise_for_status()
        data = response.json()
        webapp_url = data.get("url")

        if not webapp_url:
            await message.answer("Ошибка: URL веб-приложения не найден.")
            return

        # Создание кнопки для открытия веб-приложения
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Открыть каталог", web_app=WebAppInfo(url=webapp_url))]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )

        await message.answer(
            "Нажмите на кнопку ниже, чтобы открыть каталог акций!",
            reply_markup=keyboard
        )

    except requests.exceptions.RequestException as e:
        await message.answer(f"Не удалось связаться с бэкендом. Ошибка: {e}")
    except Exception as e:
        await message.answer(f"Произошла непредвиденная ошибка: {e}")

async def main():
    await start_polling()