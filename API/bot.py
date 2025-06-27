import os
from flask import Flask, request
import telebot
import serverless_wsgi
from werkzeug.middleware.proxy_fix import ProxyFix

# Твой токен бота (желательно хранить в переменных окружения на Vercel)
API_TOKEN = os.environ.get("API_TOKEN", "7727175707:AAEfv_J3tbPcBscm4lu3W7yRbCK3gUo3wfk")
WEBHOOK_URL = f"https://testwebhuk-dusky.vercel.app/{API_TOKEN}"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Маршрут должен совпадать с частью URL, указанного при установке вебхука
@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_data(as_text=True))
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    web_app_info = telebot.types.WebAppInfo(url="https://x-0-pi.vercel.app/")
    button = telebot.types.InlineKeyboardButton(text="PLAY🕹️", web_app=web_app_info)
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку чтобы открыть приложение.", reply_markup=markup)

# Точка входа для Vercel
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

# Локальный запуск для тестирования
if __name__ == '__main__':
    # Выставляем вебхук (один раз вручную или программно)
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    
    # Запуск локально
    app.run(debug=True, port=5000)