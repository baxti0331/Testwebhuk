import os
from flask import Flask, request
import telebot
import serverless_wsgi
from werkzeug.middleware.proxy_fix import ProxyFix

# Задайте API_TOKEN и WEBHOOK_URL через переменные окружения в Vercel
API_TOKEN = os.environ.get("API_TOKEN", "YOUR_TELEGRAM_API_TOKEN")
# WEBHOOK_URL должен указывать на публичный URL вашего деплоя на Vercel, например: https://your-deployment.vercel.app/api/bot
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://your-deployment.vercel.app/api/bot")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Маршрут функции (обратите внимание, что указывать /api/bot не нужно, Vercel уже направит запросы из этой папки)
@app.route("/", methods=["POST"])
def webhook():
    # Чтение update от Telegram
    update = telebot.types.Update.de_json(request.get_data(as_text=True))
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    web_app_info = telebot.types.WebAppInfo(url="https://x-0-pi.vercel.app/")
    button = telebot.types.InlineKeyboardButton(text="PLAY🕹️", web_app=web_app_info)
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми Кнопку чтобы открыть приложение.", reply_markup=markup)

# Точка входа для Vercel
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

if __name__ == '__main__':
    # Локальный запуск для тестирования
    app.run(debug=True, port=5000)
