import os
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    CommandHandler,
    filters,
    ChatMemberHandler
)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # توی رندر به عنوان secret environment تعریف کن

# لیست جوک‌ها و ایده‌ها
jokes = [
    "یه ربات رفتم سر کار، گفتن چرا اینقدر آهنی هستی؟ گفتم رباتم دیگه!",
    "به یه ربات گفتم سلام، گفت سلامتی هم نباشه آدم نمیشه!",
    "وقتی کامپیوتر عاشق بشه، دلش از رم می‌ره!",
]
ideas = [
    "بیاید چالش عکس پروفایل بذاریم!",
    "بازی بله/خیر توی گروه راه بندازیم؟",
    "هرکی یه حقیقت بگه که کمتر کسی بدونه!",
]

active = True  # وضعیت فعال یا خاموش بودن ربات

# وقتی عضو جدید وارد گروه میشه
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=f"""🌟 خوش اومدی {member.full_name}!
من جغدی هستم 🦉

دستورهای من:
- بگو: جغدی یه جوک بگو
- بگو: جغدی یه ایده بده
- خاموشم کن: khamoosh
- روشنم کن: roshaan

فقط وقتی اول پیام بنویسی "جغدی" جواب می‌دم!
"""
        )

# پیام‌های معمولی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active
    msg = update.message.text.strip().lower()

    if msg == "khamoosh":
        active = False
        await update.message.reply_text("🦉 جغدی خاموش شد!")
        return

    if msg == "roshaan":
        active = True
        await update.message.reply_text("🦉 جغدی دوباره روشن شد!")
        return

    if not active:
        return

    if not msg.startswith("جغدی"):
        return

    # حذف کلمه "جغدی" از اول پیام
    content = msg.replace("جغدی", "", 1).strip()

    if "جوک" in content:
        await update.message.reply_text(random.choice(jokes))
    elif "ایده" in content:
        await update.message.reply_text(random.choice(ideas))
    elif "سلام" in content:
        await update.message.reply_text("سلام رفیق! جغدی در خدمتته 🦉")
    elif "چه خبر" in content:
        await update.message.reply_text("همه چی آرومه، تو خوبی؟")
    else:
        # چیزی نگه اگه متوجه نشد
        return


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
