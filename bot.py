import telebot
import threading
import time
import os
import requests

bot_token = "6491778406:AAF2CjOcwnEfsGfiCy4daz6TlvKKPthkwwM"  # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot(token=bot_token)

chat_id = 2109538484
signal = True
@bot.message_handler(commands=['start'])
def send_hello_message(a=""):
    global chat_id, signal  # Здесь вы можете использовать любой способ хранения chat_id
    file_path = "content/report.txt"
    if signal:
        with open(file_path, "r", encoding="utf-8") as file:
            message = "Распознаное действие : " + file.readline()
            bot.send_message(chat_id, message)
        signal = False


def warning():
    global signal
    signal = True
# Функция для периодической отправки сообщений раз в минуту
def schedule_messages():
    try:
        while True:
            file_path = "content/report.txt"
            if os.path.getsize(file_path) > 0:
                send_hello_message()
            time.sleep(3) # Пауза в 60 секунд
    except KeyboardInterrupt:
        pass # Обработка прерывания (Ctrl+C)


def is_internet_available():
    timeout = 5
    try:
        _ = requests.get('http://www.google.com', timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

def start_bot():
    if is_internet_available():
        initial_message = "Start bot: AIM"
        bot.send_message(chat_id, initial_message)
        schedule_messages()
        bot.infinity_polling()
    else:
        print("Bot will not start because there is no internet connection.")


bot_thread = threading.Thread(target=start_bot)
bot_thread.start()


