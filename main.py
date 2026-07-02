import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")

def consultar_cpf(cpf):
    url = f"https://apisbrasilpro.site/api3/consulta.php?action=cpf&cpf={cpf}"
    return requests.get(url).text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Envie um CPF para consulta 👇")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cpf = update.message.text.strip()
    resultado = consultar_cpf(cpf)
    await update.message.reply_text(resultado)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
