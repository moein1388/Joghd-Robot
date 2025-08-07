import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from brain import get_chatgpt_reply, load_memory, save_memory
import datetime

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
memory = load_memory()

def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 11:
        return "صبحت بخیر جغد جان... فقط من هنوز خوابم میاد 😴"
    elif 11 <= hour < 17:
        return "ظهر شد! وقت فسفر سوزوندنه 🔥🧠"
    elif 17 <= hour < 21:
        return "عصر بخیر! یه گپ جغدی بزنیم؟ 🦉"
    else:
        return "شب شد... وقت پر زدن جغدی 🦉🌌"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_name = update.message.from_user.first_name
    memory[user_id] = {"name": user_name}
    save_memory(memory)
    
    greeting = get_greeting()
    await update.message.reply_text(
        f"سلام {user_name} عزیز! من جغد مودب و باهوشم 🤖🦉\n{greeting}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_message = update.message.text.strip()
    
    # یادگیری نام
    if user_id not in memory:
        memory[user_id] = {"name": update.message.from_user.first_name}
        save_memory(memory)
    
    user_name = memory[user_id]["name"]

    # اگر گفت "اسم من ..."
    if user_message.startswith("اسم من") or "منو صدا بزن" in user_message:
        name = user_message.split()[-1]
        memory[user_id]["name"] = name
        save_memory(memory)
        await update.message.reply_text(f"حتماً! از این به بعد صدات می‌زنم {name} 🌟")
        return

    await update.message.chat.send_action(action="typing")
    response = get_chatgpt_reply(user_name, user_message)
    await update.message.reply_text(response)

if name == 'main':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ ربات جغد متفکر راه افتاد...")
    app.run_polling()
