from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# тут будемо писати наш код :)

TOKEN = "7085486431:AAFuvGIUJ7_ueMU8EzClrxED9p11yYTTLps"

async def start(update, context):
    dialog.mode = "None"
    msg = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, msg)
    await show_main_menu(update, context, {
        "start": "Головне меню",
        "profile": "Генерація Tinder-профіля \uD83D\uDE0E",
        "opener": "Повідомлення для знайомства \uD83E\uDD70",
        "message": "Переписка від вашого імені \uD83D\uDE08",
        "date": "Спілкування з зірками \uD83D\uDD25",
        "gpt": "Задати питання ChatGPT \uD83E\uDDE0"
    })

async def gpt(update, context):
    dialog.mode = "gpt"
    await send_photo(update, context, "gpt")
    await send_text(update, context, load_message("gpt"))

async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)

async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)

dialog = Dialog()
dialog.mode = "None"

chatgpt = ChatGptService(token="gpt:AwXimzQXBV8upnlD2Fs0exPWVNTK9gmJGa_-erhzfPL1q5ldKc7zlb9PU53QlMYgrXBnjxK1uVJFkblB3TVSZ57z3Zm705v8y2sd9IG54evj_wDJ-zeNy_W7xT6lcYEGbp9qD9IbKvgZ5Ks22k_pKNEe74Sd")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.run_polling()
