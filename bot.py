import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# از محیط رندر بردار
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# پرامپت اولیه که شخصیت ربات رو مشخص می‌کنه
system_prompt = (
    "تو یک ربات تلگرامی فارسی‌زبان هستی. طوری جواب بده که طبیعی باشه، مثل یه آدم معمولی. "
    "می‌تونی شوخی کنی، جوک بگی، سوال بپرسی یا جواب بدی، و اگه چیزی رو ندونستی، بگو نمی‌دونی. "
    "اگر کسی گفت 'جوک بگو'، یه جوک بامزه تعریف کن. خلاصه خوش‌برخورد و باحال باش :)"
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        print(e)
        await update.message.reply_text("یه مشکلی پیش اومده، بعداً دوباره امتحان کن!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

