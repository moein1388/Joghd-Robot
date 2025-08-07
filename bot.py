import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random

# جوک‌ها و پاسخ‌ها
jokes = [
    "می‌دونی چرا مرغ از خیابون رد شد؟ چون اون طرفش اینترنت رایگان بود!",
    "یه بار یه گوسفند رفت دانشگاه، استاد شد!",
    "یه ربات دیدم انقدر باهوش بود خودش رو خاموش کرد که با آدم‌ها بحث نکنه!",
]

answers = {
    "چه خبر": "سلامتی! تو چه خبر؟ 😄",
    "خوبی": "مرسی که پرسیدی! همیشه خوبم اگه گروه خوب باشه!",
    "جوک بگو": lambda: random.choice(jokes),
    "سلام": "سلام رفیق! خوش اومدی! 🌟",
}

# حالت فعال یا غیرفعال
ACTIVE = True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من جغدی‌ام 🦉\n"
        "فقط وقتی پیامت با «جغدی» شروع بشه جواب می‌دم.\n"
        "دستورها:\n"
        "- joghdi khamoosh (خاموش می‌کنم خودمو)\n"
        "- joghdi roshan (دوباره فعال می‌شم)"
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ACTIVE
    text = update.message.text.lower()

    if not text.startswith("joghdi"):
        return  # فقط به پیام‌هایی که با "جغدی" شروع میشن جواب می‌ده

    command = text[6:].strip()  # حذف "joghdi"

    if "khamoosh" in command:
        ACTIVE = False
        await update.message.reply_text("چشم، ساکت می‌مونم. 💤")
        return

    if "roshan" in command:
        ACTIVE = True
        await update.message.reply_text("من برگشتم! 🦉")
        return

    if not ACTIVE:
        return

    # پاسخ دادن به دستورات ساده
    for key in answers:
        if key in command:
            response = answers[key]
            if callable(response):
                response = response()
            await update.message.reply_text(response)
            return

    # اگه نفهمید، هیچ چی نمی‌گه
    return

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"به گروه خوش اومدی {member.first_name}!\n"
            "من جغدی‌ام 🦉، اگه خواستی باهام حرف بزنی اول پیام بگو: joghdi\n"
            "مثلاً:\n"
            "- joghdi جوک بگو\n"
            "- joghdi چه خبر\n"
            "- joghdi khamoosh / roshan"
        )

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("Please set your BOT_TOKEN environment variable.")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
