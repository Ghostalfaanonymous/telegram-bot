import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# TOKEN vindo do Render
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN não configurado no Render!")


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot online!\n\nUse:\n/cpf 12345678900"
    )


# /cpf
async def cpf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /cpf 12345678900")
        return

    cpf = context.args[0]

    url = f"http://apisbrasilpro.site/api3/consulta.php?action=cpf&cpf={cpf}"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        resposta = "🔎 RESULTADO CPF\n\n"

        for chave, valor in data.items():
            resposta += f"{chave}: {valor}\n"

        await update.message.reply_text(resposta)

    except Exception as e:
        await update.message.reply_text(f"❌ Erro na consulta: {e}")


# inicia bot
def main():
    print("🤖 Bot iniciado...")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cpf", cpf))

    app.run_polling()


if __name__ == "__main__":
    main()
