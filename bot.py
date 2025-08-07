from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import random
import os
import openai  # تغییر اینجا

# بارگذاری متغیرهای محیطی (اگر از dotenv استفاده می‌کنی)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

openai.api_key = GROQ_API_KEY
openai.api_base = "https://api.groq.com/openai/v1"  # آدرس پایه API گراگ

greetings = ["سلام بر جغد شب‌زنده‌دار 🌙", "درود بر تو جغد عزیز 🦉", "سلام رفیق جغدی 😄"]
funny_responses = [
    "الان وقت جغد بودنه یا فسفر سوزوندن؟ 🦉",
    "تو جغدی یا انسان نمای شب‌زنده‌دار؟ 😂",
    "سوری بیا ببین کی اومده! 😏",
    "باز تو اومدی؟ من آماده‌م برای شوخی! 😎",
]
questions_responses = [
    "سوالی بود؟ من همیشه پایه‌ام برای جواب 🎓",
    "بپرس عزیز دل، جغدها باس باس باشن 😌",
    "شاید بلد نباشم ولی تلاشمو می‌کنم 🧠",
]
unknown_responses = [
    "🧠 هنوز دارم یاد می‌گیرم، ولی سعی می‌کنم بفهمم چی گفتی!",
    "من نفهمیدم دقیق چی گفتی ولی خوشم اومد از حرفت 😄",
    "یه بار دیگه بگو، انگار حافظه‌م پر بود 😂",
]

async def get_groq_response(user_message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "تو یه ربات مودب و شوخ تلگرام هستی."},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"خطا در ارتباط با Groq: {e}")
        return "متأسفم الان نمی‌تونم جواب بدم!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات جغد مودبم 🦉 آماده‌ام برای چت، شوخی، رأی‌گیری و سرگرمی!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user.first_name or "رفیق"

    if "استیکر بده" in text or "استیکر بفرست" in text:
        await update.message.reply_sticker(
            "CAACAgUAAxkBAAEBJxZkZJNmX8r3oD5zAq-6EVrJIXsAASsAAp5QGFWkiu5nL0ewDzUE"
        )
        return

    if "ویس بده" in text or "صدا بفرست" in text:
        voice_path = "voice.ogg"
        if os.path.exists(voice_path):
            await update.message.reply_voice(
                voice=InputFile(voice_path), caption="ویس جغدی 🎤🦉"
            )
        else:
            await update.message.reply_text("فعلاً ویس ندارم 😢 یه فایل voice.ogg کنارم بذار")
        return

    if text.lower().startswith("/start"):
        await start(update, context)
        return

    if "رای‌گیری" in text or "رأی‌گیری" in text:
        await update.message.reply_poll(
            question=f"{user} یه رأی‌گیری راه انداخت 🗳️",
            options=["آره", "نه", "بی‌خیال"],
            is_anonymous=False,
        )
        return

    if "سلام" in text.lower():
        await update.message.reply_text(random.choice(greetings))
        return

    bot_reply = await get_groq_response(text)
    await update.message.reply_text(bot_reply, reply_to_message_id=update.message.message_id)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ ربات جغد مودب هوشمند آماده است!")
    app.run_polling()

