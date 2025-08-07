import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random

# وضعیت خاموش/روشن
is_active = True  # پیش‌فرض: روشنه

# پاسخ‌ها بر اساس کلمات کلیدی
responses = {
    "سلام": ["سلام رفیق! خوبی؟", "سلام به روی ماهت 😎", "سلام، چه خبرا؟"],
    "چه خبر": ["هیچی والا، مشغول ربات‌بازی! تو چی؟", "همه چی آرومه..."],
    "حوصله": ["بیا یه جوک بشنو حوصلت سر نره 😄", "یه بازی کنیم؟ من بلدم!"],
    "جوک": ["رفیق، یه مورچه می‌خواست بره خواستگاری فیل، فیل گفت بابام نمی‌ذاره!"],
    "ایده": ["یه چالش عکس پروفایل بندازیم؟", "بیاید بازی حقیقت یا جرئت بزنیم تو گروه!"],
    "سوری": ["جانم؟ من همیشه اینجام 😎"],
    "چیکار کنم": ["بیا با من حرف بزن، حوصله‌ات سر نره!", "می‌خوای جوک بگم؟ یا بریم سراغ ایده‌ها؟"],
    "بازی": ["بازی کنیم؟ اوکی! بگو 'سنگ کاغذ قیچی' یا 'سوال جواب'"],
    "دوست دارم": ["منم دوستت دارم رفیق ❤️"],
}

default_responses = [
    "جالب بود حرفت! بیشتر بگو 😄",
    "من هنوز مغز واقعی ندارم ولی دارم تمرین می‌کنم!",
    "اگه دوست داشتی جوک یا ایده بگو 😎"
]

# مدیریت پیام‌ها
async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_active
    text = update.message.text.lower()

    if text == "khamoosh":
        is_active = False
        await update.message.reply_text("باشه، دیگه ساکت می‌شم 🤐")
        return
    elif text == "roshaan":
        is_active = True
        await update.message.reply_text("دوباره روشن شدم 😎 بگو ببینم چی شده؟")
        return

    if not is_active:
        return  # سکوت در حالت خاموش

    # چک کردن کلمات کلیدی
    for keyword in responses:
        if keyword in text:
            await update.message.reply_text(random.choice(responses[keyword]))
            return

    # اگر هیچ چیز رو نفهمید، سکوت کنه (هیچی نگه)
    return

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من یه ربات اجتماعی هستم. بگو چی دوست داری؟")

# خوش‌آمدگویی به افراد جدید
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "🌟 به گروه خوش اومدی!\n"
        "من یه ربات اجتماعی هستم.\n"
        "می‌تونی باهام حرف بزنی مثل:\n"
        "- سلام\n"
        "- جوک بده\n"
        "- یه ایده بده\n"
        "- بگو چه خبر؟\n"
        "\n"
        "برای کنترل من:\n"
        "🔕 خاموشم کن: khamoosh\n"
        "🔔 روشنم کن: roshaan"
    )
    await update.message.reply_text(welcome_msg)

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")  # توکن از محیط
    if not TOKEN:
        print("❌ BOT_TOKEN در محیط تعریف نشده.")
    else:
        app = ApplicationBuilder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply_handler))

        print("✅ ربات روشنه...")
        app.run_polling()
