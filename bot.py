import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# خواندن توکن‌ها از متغیرهای محیطی
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

bot_active = True
active_conversations = {}
chat_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == 'private':
        await update.message.reply_text(
            "سلام! خوش اومدی! لطفاً ربات رو به گروهی که می‌خوای اضافه کن."
        )
    else:
        await update.message.reply_text("سلام! من اینجا هوشمندانه چت می‌کنم.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_active
    chat_id = update.message.chat.id
    user_text = update.message.text.lower()

    if not bot_active:
        if "جغد بیدار" in user_text:
            bot_active = True
            await update.message.reply_text("ربات دوباره روشن شد! 🦉")
        else:
            return
        return

    if "جغد بخواب" in user_text:
        bot_active = False
        await update.message.reply_text("ربات خاموش شد! برای روشن شدن 'جغد بیدار' رو بگو.")
        return

    if update.message.chat.type == 'private':
        if user_text == '/start':
            await update.message.reply_text(
                "سلام! خوش اومدی! لطفاً ربات رو به گروهی که می‌خوای اضافه کن."
            )
        return

    if update.message.chat.type in ['group', 'supergroup']:
        if chat_id not in active_conversations:
            if "جغدی" in user_text:
                active_conversations[chat_id] = True
                chat_histories[chat_id] = [
                    {"role": "system", "content": "تو یک ربات مودب و شوخ تلگرامی هستی."},
                ]
                await update.message.reply_text("سلام! جغدی هستم، بگو چی می‌خوای!")
            else:
                return
        else:
            if "بسه جغدی" in user_text:
                active_conversations.pop(chat_id, None)
                chat_histories.pop(chat_id, None)
                await update.message.reply_text("باشه، مکالمه تموم شد. هر وقت خواستی بگو 'جغدی' دوباره شروع کنیم.")
                return

            history = chat_histories.get(chat_id)
            history.append({"role": "user", "content": user_text})

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=history,
                    max_tokens=200,
                    temperature=0.8,
                )
                bot_reply = response.choices[0].message['content']
                history.append({"role": "assistant", "content": bot_reply})
                chat_histories[chat_id] = history[-10:]
            except Exception:
                bot_reply = "متأسفانه الان نمی‌تونم جواب بدم."

            await update.message.reply_text(bot_reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ربات جغد مودب آماده به کار است!")
    app.run_polling()

