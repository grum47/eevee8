import json

from working_hours import working_hours_buttons, time_work_func, get_today_last_event, get_today_working_hours
from func import write_log

with open("./eevee8/config.json") as conf:
    data = json.loads(conf.read())
    token = data['token']

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Определяем логику команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Учет рабочего времени", callback_data='working_hours'),
         InlineKeyboardButton("Тренировка", callback_data='training')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите опцию:', reply_markup=reply_markup) # type: ignore


# Кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # type: ignore

    # WORKING HOURS
    if query.data == 'working_hours': # type: ignore
        await working_hours_buttons(query=query)
    
    elif query.data == 'last_event': # type: ignore
        last_event = await get_today_last_event()
        await query.edit_message_text(text=f"Последнее событие: {last_event.upper()}") # type: ignore
    
    elif query.data in ['start_work', 'end_work']: # type: ignore
        await time_work_func(query.data) # type: ignore
    
    elif query.data == 'today_working': # type: ignore
        working_hours, working_minuts = await get_today_working_hours()
        await query.edit_message_text(text=f"Сегодня отработано: {working_hours}:{working_minuts}") # type: ignore
    
    # TRAINING
    elif query.data == 'training': # type: ignore
        await query.edit_message_text(text="Опция в разработке") # type: ignore

# Запуск бота
if __name__ == '__main__':
    try:
        application = ApplicationBuilder().token(token).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))

        application.run_polling()

    except Exception as e:
        write_log(message=str(e))
