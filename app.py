import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.utils.executor import start_webhook
from fastapi import FastAPI
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

# Получение токена из .env
BOT_TOKEN = os.getenv("BOT_TOKEN", "7563958637:AAFWLdH8ok1EVc4SF8OJTEcv6UCV2aZMqIA")  # Замените на ваш токен, если не используете .env
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"https://testwebhuk.vercel.app{WEBHOOK_PATH}"  # Ваш домен на Vercel

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Убедитесь, что он указан в переменных окружения или .env файле")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Создание FastAPI приложения
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Установка вебхука
    await bot.set_webhook(WEBHOOK_URL)
    # Установка команд бота
    await bot.set_my_commands([
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/help", description="Помощь")
    ])

@app.on_event("shutdown")
async def on_shutdown():
    # Удаление вебхука при завершении
    await bot.delete_webhook()

@app.post(WEBHOOK_PATH)
async def process_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.process_update(telegram_update)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Я Telegram-бот. Чем могу помочь?")

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer("Доступные команды:\n/start - Запуск бота\n/help - Помощь")

@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")