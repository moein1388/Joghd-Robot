from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import cleverbot_free

TOKEN = "8350519810:AAGneRC9rpyiEs1kwagmlTvca3yNQrbamIA"

cb = cleverbot_free.Cleverbot()

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        bot_response = await cb.single_exchange(user_message)
    except:
        bot_response = "متأسفم الان نمی‌تونم جواب بدم!"
    await update.message.reply_text(bot_response)

if name == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("ربات هوشمند داره کار می‌کنه...")
    app.run_polling()
