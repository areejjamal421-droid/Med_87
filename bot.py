import os
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv('9100262932:AAHUo79g_vKxOPTWmPXAnj2mXhVIwN-PBdU')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# قائمة المواد وشيتاتها (يمكنك تعديل الروابط والأسماء براحتك)
subjects_data = {
    "ماتيريال": [
        "شيت ماتيريال 1: https://t.example.com/material1.pdf",
        "شيت ماتيريال 2: https://t.example.com/material2.pdf",
        "ملخص الماتيريال الشامل: https://t.example.com/material_summary.pdf"
    ],
    "اناتومي": [
        "شيت أناتومي 1: https://t.example.com/anatomy1.pdf",
        "شيت أناتومي 2: https://t.example.com/anatomy2.pdf"
    ],
    "بايوكيمستري": [
        "شيت بايوكيمستري المحاضرة الأولى: https://t.example.com/bio1.pdf",
        "شيت بايوكيمستري المحاضرة الثانية: https://t.example.com/bio2.pdf"
    ],
    "هستو": [
        "شيت هستو 1: https://t.example.com/histo1.pdf"
    ],
    "فسيو": [
        "شيت فسيو 1: https://t.example.com/physio1.pdf"
    ],
    "باثو": [
        "شيت باثو 1: https://t.example.com/patho1.pdf"
    ],
    "ميكرو": [
        "شيت ميكرو 1: https://t.example.com/micro1.pdf"
    ]
}

@app.route('/')
def home():
    return "Medical Bot is active!"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# أمر البدء بالرسالة الترحيبية الجديدة وعرض المواد كأزرار تحت بعضها
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    for subject in subjects_data.keys():
        markup.add(InlineKeyboardButton(text=subject, callback_data=f"sub_{subject}"))
    
    bot.send_message(
        message.chat.id, 
        "أهلاً بك يَ دكتور 🩶\nاختر المادة لعرض جميع الشيتات الخاصة بها:", 
        reply_markup=markup
    )

# استقبال الضغطة وإرسال كافة شيتات المادة معاً
@bot.callback_query_handler(func=lambda call: call.data.startswith('sub_'))
def callback_inline(call):
    subject_name = call.data.replace('sub_', '')
    if subject_name in subjects_data:
        sheets_list = subjects_data[subject_name]
        response_text = f"📚 **شيتات مادة ({subject_name}):**\n\n" + "\n".join(sheets_list)
        bot.answer_callback_query(call.id, f"تم جلب شيتات {subject_name}")
        bot.send_message(call.message.chat.id, response_text)
    else:
        bot.answer_callback_query(call.id, "عذراً، المادة غير متوفرة حالياً.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f'https://اسم-خدمتك.onrender.com/{TOKEN}')
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
