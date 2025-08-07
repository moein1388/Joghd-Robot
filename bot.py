from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

TOKEN = "8350519810:AAGneRC9rpyiEs1kwagmlTvca3yNQrbamIA"

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

chat_history = {}

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id

    # بازیابی تاریخچه چت برای هر کاربر
    history = chat_history.get(chat_id)

    new_input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')

    if history is not None:
        bot_input_ids = torch.cat([history, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    output_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    chat_history[chat_id] = output_ids

    bot_response = tokenizer.decode(output_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    await update.message.reply_text(bot_response)

if name == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("ربات هوشمند داره کار می‌کنه...")
    app.run_polling()
