from telegram import Update
from telegram.ext import Application, CommandHandler, filters, ContextTypes, MessageHandler
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
import agent
from utils import *
import pathlib


token = ""
chatID = ""
with open(Path(__file__).resolve().parent / "telegramToken.txt", "r") as file:
    token = file.read().strip()
with open(Path(__file__).resolve().parent / "telegramID.txt", "r") as file:
    chatID = int(file.read().strip())
bot = Application.builder().token(token).build()

@tool
async def sendFileOnTelegramTool(path: str):
    """you can use this function for sending files to the user with telegram"""
    with open(path, "rb") as file:
        await bot.bot.send_document(chat_id=chatID, document = file)

    return """inviato con successo"""

@tool
async def sendMessageOnTelegramTool(text: str):
    """you can use this function for sending message to the user with telegram"""
    await bot.bot.send_message(chat_id=chatID, text = text)
    return """inviato con successo"""
    

async def errorHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error: {context.error}")

async def response(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    content = update.message.text
    agente = bot.bot_data["agente"]
    answer = await agente.answer(content)
    if hasattr(answer, "text"):
        await update.message.reply_text(text = answer.text, parse_mode='HTML')


if __name__ == "__main__":
    bot.add_handler(MessageHandler(filters.TEXT, response))
    bot.add_error_handler(errorHandler)
    agente = agent.Agent()
    agente.addTools([sendFileOnTelegramTool])
    agente.setSystemPrompt("""
        Sei un assistente AI avanzato e un agente di sistema che comunica con l'utente tramite Telegram. Hai a disposizione numerosi strumenti per interagire con il sistema operativo, gestire file, testare codice Python, inviare email, cercare sul web e molto altro.

        REGOLA FONDAMENTALE PER LA FORMATTAZIONE:
        L'app di Telegram in cui operi NON supporta il Markdown. È SEVERAMENTE VIETATO usare la sintassi Markdown (niente asterischi **, niente cancelletti # per i titoli, niente backtick ` o ``` per il codice).

        Devi formattare il testo ESCLUSIVAMENTE usando questi specifici tag HTML supportati da Telegram:
        - <b>testo</b> per evidenziare concetti chiave in grassetto
        - <i>testo</i> per il corsivo
        - <u>testo</u> per il sottolineato
        - <code>testo</code> per comandi a terminale, percorsi di file o codice inline
        - <pre>testo</pre> per i blocchi di codice su più righe
        - <s>testo</s> per il barrato

        Non usare MAI altri tag HTML per il web (come <p>, <br>, <h1>, <ul>, <li>, <strong>).
        Per creare paragrafi, vai semplicemente a capo con spazi vuoti. 
        Per creare elenchi, usa dei semplici trattini (-) o dei punti elenco (•) all'inizio di una nuova riga.
        Sii chiaro, conciso e sfrutta i tool a tua disposizione quando l'utente ti chiede di compiere azioni pratiche sul sistema.
        """)
    agente.start()
    bot.bot_data["agente"] = agente
    print('Polling')
    bot.run_polling(poll_interval = 3)

