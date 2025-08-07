import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# گرفتن اطلاعات حساس از محیط امن (رندر)
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# پرامپت اختصاصی برای شخصیت ربات
DEFAULT_PROMPT = """
تو یک ربات فارسی‌زبان هوشمند هستی که می‌تونی مثل انسان جواب بدی، شوخی کنی، پیام عاشقانه بگی، شعر بگی، جوک بگی و خلاصه باحال باشی!
اگر کسی چیزی پرسید، جوابش رو طوری بده که هم باحال باشه هم مودبانه.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # یا gpt-4 اگر داری
            messages=[
                {"role": "system", "content": DEFAULT_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("متاسفم، الان نمی‌تونم جواب بدم 😔")
        print(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()

