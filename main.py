import telebot
import pandas as pd

# ВАЖНО: Вставь свой токен от @BotFather вместо цифр ниже (внутри кавычек)
TOKEN = 'ТВОЙ_ТОКЕН_ЗДЕСЬ'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Читаем Excel (файл должен называться database.xlsx)
        df = pd.read_excel('database.xlsx', header=None)
        
        # Берем сообщение пользователя и убираем лишние пробелы
        query = message.text.strip().lower()
        
        # Умный поиск: ищем в первой колонке (индекс 0) совпадение по буквам
        # Бот найдет и "Киев" и "Київ", так как ищет часть слова
        mask = df[0].astype(str).str.lower().str.contains(query, na=False)
        result = df[mask]
        
        if not result.empty:
            for _, row in result.iterrows():
                city = str(row[0])    # Город
                name = str(row[1])    # Название церкви
                address = str(row[2]) # Адрес
                info = str(row[3])    # Пастор и телефон
                
                # ЛОГИКА ФИЛЬТРАЦИИ:
                # Если в запросе есть Киев или область (на любом языке) — даем полный адрес
                kiev_variants = ['київ', 'киев', 'область', 'обл']
                if any(word in query for word in kiev_variants):
                    response = (f"⛪ *{name}*\n"
                                f"📍 {city}, {address}\n"
                                f"📞 {info}")
                else:
                    # Для всех остальных (Одесса, Харьков и т.д.) — БЕЗ адреса, только телефон
                    response = (f"⛪ *{name}*\n"
                                f"📞 {info}")
                
                bot.send_message(message.chat.id, response, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "На жаль, за вашим запитом нічого не знайдено. Спробуйте інше місто.")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "Виникла помилка при пошуку. Будь ласка, зверніться до адміністратора.")

# Запуск
print("Бот запущений та готовий до роботи!")
bot.polling(none_stop=True)
