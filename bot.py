import os
from flask import Flask
from threading import Thread
import telebot

# --- سيرفر الويب الوهمي للبقاء 24/7 ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# --- كود بوت التليجرام ---
TOKEN = "9100262932:AAHUo79g_vKxOPTWmPXAnj2mXhVIwN-PBdU"  # ضع توكن بوتك الجديد هنا
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا دكتور في البوت الطبي الجديد والشغال 24/7! 🩺")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling(skip_pending=True)
