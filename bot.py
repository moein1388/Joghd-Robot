import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters, ChatMemberHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # توکن رو از محیط می‌خونه
ACTIVE = True  # حالت روشن/خاموش

# پیام خوش‌آمد برای اعضای جدید
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        await update.effective_chat.send_message(
            f"سلام {member.first_name} 👋\nمن جغدی‌ام! 🦉\n"
            "برای حرف زدن با من باید اول اسمم رو صدا بزنی:\nمثلاً:\nجغدی چه خبر؟\n"
            "دستورهای من:\n• khamoosh → خاموش می‌شم\n• roshaan → روشن می‌شم"
        )

# پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ACTIVE

    if not update.message:
        return

    msg = update.message.text.lower()

    if not msg.startswith("جغدی"):
        return

    cmd = msg.replace("جغدی", "").strip()

    if "khamoosh" in cmd:
        ACTIVE = False
        await update.message.reply_text("🛑 خاموش شدم. دیگه حرف نمی‌زنم.")
    elif "roshaan" in cmd:
        ACTIVE = True
        await update.message.reply_text("✅ روشن شدم. دوباره برگشتم!")
    elif not ACTIVE:
        return
    elif any(word in cmd for word in ["چه خبر", "سلام", "خوبی"]):
        await update.message.reply_text("سلام رفیق! من جغدی‌ام، چه خبر از تو؟ 🦉")
    elif "جوک" in cmd:
        await update.message.reply_text("یه بار یه ربات عاشق شد، رفت با پریز برق ازدواج کرد 😂")
    elif "ایده" in cmd:
        await update.message.reply_text("بیاید یه چالش عکس پروفایل برگزار کنیم!")
    else:
        await update.message.reply_text("من متوجه نشدم، ولی اگه بخوای سعی می‌کنم یاد بگیرم 🤖")

# اجرای ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()
