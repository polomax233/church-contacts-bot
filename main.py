import telebot
import pandas as pd
from flask import Flask
from threading import Thread

# 1. МИНИ-СЕРВЕР ДЛЯ RENDER
app = Flask('')
@app.route('/')
def home():
    return "Бот працює!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. НАСТРОЙКИ БОТА
TOKEN = 'ТВОЙ_ТОКЕН' # Проверь, чтобы тут был твой токен!
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        df = pd.read_excel('database.xlsx', header=None)
        query = message.text.strip().lower()
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
        result = df[mask]
        
        if not result.empty:
            for _, row in result.iterrows():
                city, name, address, info = str(row[0]), str(row[1]), str(row[2]), str(row[3])
                if any(k in query for k in ['київ', 'киев', 'область']):
                    text = f"⛪ *{name}*\n📍 {city}, {address}\n📞 {info}"
                else:
                    text = f"⛪ *{name}*\n📞 {info}"
                bot.send_message(message.chat.id, text, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "На жаль, нічого не знайдено.")
    except Exception as e:
        print(f"Ошибка: {e}")

# ЗАПУСК
if __name__ == "__main__":
    keep_alive() # Запускаем мини-сервер для Render
    print("Бот запущений!")
    bot.polling(none_stop=True)
