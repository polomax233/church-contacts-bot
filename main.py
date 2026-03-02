python
import telebot
import pandas as pd

# ВАЖНО: Вместо цифр ниже вставь свой токен от @BotFather (внутри кавычек)
TOKEN = 'ТУТ_ТВОЙ_ТОКЕН_ОТ_BOTFATHER'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Читаем твой Excel (файл должен называться database.xlsx)
        # Мы говорим боту, что заголовков нет, используем колонки 0, 1, 2, 3
        df = pd.read_excel('database.xlsx', header=None)
        
        query = message.text.strip().lower()
        
        # Ищем город в первой колонке (индекс 0)
        # Сделаем поиск по всей строке на всякий случай
        mask = df[0].astype(str).str.lower().contains(query, na=False)
        result = df[mask]
        
        if not result.empty:
            for _, row in result.iterrows():
                city = str(row[0])    # Город
                name = str(row[1])    # Название церкви
                address = str(row[2]) # Адрес
                info = str(row[3])    # Пастор и телефон
                
                # Логика: Киев и область — всё. Одесса/Харьков — только инфо.
                if 'киев' in query or 'київ' in query:
                    response = f"⛪ {name}\n📍 {city}, {address}\n📞 {info}"
                else:
                    # Для Одессы, Харькова и других — только телефон/пастор
                    response = f"⛪ {name}\n📞 {info}"
                
                bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "По этому городу ничего не найдено. Попробуйте написать по-другому.")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при поиске. Проверьте базу данных.")

bot.polling(none_stop=True)
