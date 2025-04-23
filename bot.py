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


async def date(update, context):
    dialog.mode = "date"
    msg = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, msg, {
        "date_grande": "Аріана Гранде",
        "date_robbie": "Марго Роббі",
        "date_zendaya": "Зендея",
        "date_gosling": "Райан Гослінг",
        "date_hardy": "Том Харді"
    })


async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    await send_photo(update, context, query)
    await send_text(update, context,
                    "Гарний вибір! \uD83D\uDE05 Ваше завдання запросити дівчину або хлопця на побачення за 5 повідомлень!💝")
    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)


async def date_dialog(update, context):
    text = update.message.text
    wait_message = await send_text(update, context, "Набирає .....")
    answer = await chatgpt.add_message(text)
    await wait_message.edit_text(answer)


async def message(update, context):
    dialog.mode = "message"
    msg = load_message("message")
    await send_photo(update, context, "message")
    await send_text_buttons(update, context, msg, {
        "message_next": "Написати повідомлення",
        "message_date": "Запросити на побачення"
    })
    dialog.list.clear()


async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)
    wait_message = await send_text(update, context, "Розмірковую над варіантами .......")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await wait_message.edit_text(answer)


async def profile(update, context):
    dialog.mode = "profile"
    msg = load_message("profile")
    await send_photo(update, context, "profile")
    await send_text(update, context, msg)

    dialog.user.clear()
    dialog.counter = 0

    await send_text(update, context, "Скільки Вам років?")



async def profile_dialog(update, context):
    text = update.message.text
    dialog.counter += 1

    if dialog.counter == 1:
        dialog.user["age"] = text
        await send_text(update, context, "Ким ви працюєте?")
    elif dialog.counter == 2:
        dialog.user["occupation"] = text
        await send_text(update, context, "Яку ви маєте хобі?")
    elif dialog.counter == 3:
        dialog.user["hobby"] = text
        await send_text(update, context, "Що Вам НЕ подобається в людях?")
    elif dialog.counter == 4:
        dialog.user["annoys"] = text
        await send_text(update, context, "Мета знайомства?")
    elif dialog.counter == 5:
        dialog.user["goals"] = text

        prompt = load_prompt("profile")
        user_info = dialog_user_info_to_str(dialog.user)

        wait_message = await send_text(update, context, "ChatGPT \uD83E\uDDE0 генерує Ваш профіль! Зачекайте......")
        answer = await chatgpt.send_question(prompt, user_info)
        await wait_message.edit_text(answer)


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    elif dialog.mode == "date":
        await date_dialog(update, context)
    elif dialog.mode == "message":
        await message_dialog(update, context)
    elif dialog.mode == "profile":
        await profile_dialog(update, context)


dialog = Dialog()
dialog.mode = "None"
dialog.list = []
dialog.user = {}
dialog.counter = 0

chatgpt = ChatGptService(
    token="gpt:AwXimzQXBV8upnlD2Fs0exPWVNTK9gmJGa_-erhzfPL1q5ldKc7zlb9PU53QlMYgrXBnjxK1uVJFkblB3TVSZ57z3Zm705v8y2sd9IG54evj_wDJ-zeNy_W7xT6lcYEGbp9qD9IbKvgZ5Ks22k_pKNEe74Sd")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CallbackQueryHandler(date_button, pattern="date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="message_.*"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.run_polling()
