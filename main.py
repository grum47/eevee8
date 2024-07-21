from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json


with open("./eevee8/config.json") as conf:
    data = json.loads(conf.read())
    token = data['token']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            KeyboardButton("Тренировки"),
            KeyboardButton("Учет рабочего времени")
            ],
        [
            KeyboardButton("Статистика по курсу доллара"),
            KeyboardButton("ФУНКЦИЯ")
            ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите опцию', reply_markup=reply_markup) # type: ignore

async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text # type: ignore
    if text == "Тренировки":
        await update.message.reply_text("Выбор тренировки") # type: ignore
    elif text == "Учет рабочего времени":
        await update.message.reply_text("Логика учета времени") # type: ignore
    elif text == "Статистика по курсу доллара":
        await update.message.reply_text("Запук расчета статистики по курсу") # type: ignore
    elif text == "ФУНКЦИЯ":
        pass

if __name__ == '__main__':
    application = ApplicationBuilder().token(token=token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_options))

    application.run_polling()
