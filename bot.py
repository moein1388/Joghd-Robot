from telegram import Update, Poll, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random
import os

# ✅ توکن ربات
TOKEN = '123456789:ABCDEFghijklmnop_YOUR_REAL_TOKEN_HERE'

# 🎭 لیست پاسخ‌های مختلف
greetings = ["سلام بر جغد شب‌زنده‌دار 🌙", "درود بر تو جغد عزیز 🦉", "سلام رفیق جغدی 😄"]
funny_responses = [
    "الان وقت جغد بودنه یا فسفر سوزوندن؟ 🦉",
    "تو جغدی یا انسان نمای شب‌زنده‌دار؟ 😂",
    "سوری بیا ببین کی اومده! 😏",
    "باز تو اومدی؟ من آماده‌م برای شوخی! 😎"
]
questions_responses = [
    "سوالی بود؟ من همیشه پایه‌ام برای جواب 🎓",
    "بپرس عزیز دل، جغدها باس باس باشن 😌",
    "شاید بلد نباشم ولی تلاشمو می‌کنم 🧠"
]
unknown_responses = [
    "🧠 هنوز دارم یاد می‌گیرم، ولی سعی می‌کنم بفهمم چی گفتی!",
    "من نفهمیدم دقیق چی گفتی ولی خوشم اومد از حرفت 😄",
    "یه بار دیگه بگو، انگار حافظه‌م پر بود 😂"
]

# 🎬 فرمان /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات جغد مودبم 🦉 آماده‌ام برای چت، شوخی، رأی‌گیری و سرگرمی!")

# 📝 هندلر اصلی پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.message.from_user.first_name or "رفیق"

    # پاسخ به سلام
    if 'سلام' in text:
        await update.message.reply_text(random.choice(greetings), reply_to_message_id=update.message.message_id)

    # شوخی با اسم جغد یا سوری
    elif 'جغد' in text or 'سوری' in text:
        await update.message.reply_text(random.choice(funny_responses), reply_to_message_id=update.message.message_id)

    # رأی‌گیری
    elif 'رای‌گیری' in text or 'رأی‌گیری' in text:
        await update.message.reply_poll(
            question=f"{user} یه رأی‌گیری راه انداخت 🗳️",
            options=["آره", "نه", "بی‌خیال"],
            is_anonymous=False,
        )

    # بیدار بودن
    elif 'کی بیداره' in text or 'کی آنلاینه' in text:
        await update.message.reply_text("من بیدارم 😎 جغد شب‌زنده‌دار هیچوقت نمی‌خوابه!")

    # درخواست استیکر
    elif 'استیکر بده' in text or 'استیکر بفرست' in text:
        await update.message.reply_sticker("CAACAgUAAxkBAAEBJxZkZJNmX8r3oD5zAq-6EVrJIXsAASsAAp5QGFWkiu5nL0ewDzUE")

    # درخواست ویس
    elif 'ویس بده' in text or 'صدا بفرست' in text:
        voice_path = "voice.ogg"
        if os.path.exists(voice_path):
            await update.message.reply_voice(voice=InputFile(voice_path), caption="ویس جغدی 🎤🦉")
        else:
            await update.message.reply_text("فعلاً ویس ندارم 😢 یه فایل voice.ogg کنارم بذار")

    # اگر جمله سوالی بود (علامت سوال)
    elif '?' in text or '؟' in text:
        await update.message.reply_text(random.choice(questions_responses), reply_to_message_id=update.message.message_id)

    # در غیر این صورت
    else:
        await update.message.reply_text(random.choice(unknown_responses), reply_to_message_id=update.message.message_id)

# 🚀 اجرای ربات
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ ربات جغد مودب هوشمند آماده است!")
app.run_polling()
