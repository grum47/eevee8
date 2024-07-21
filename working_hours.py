import csv
from datetime import datetime
import json
import os
import pandas as pd
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from func import write_log

file_path = './eevee8/pomodoro_stats.csv'

# Кнопки Учет работчего времени
async def working_hours_buttons(query) -> None:
    additional_keyboard = [
        [InlineKeyboardButton("Последнее событие", callback_data='last_event')],
        [InlineKeyboardButton("Начало работы", callback_data='start_work'),
         InlineKeyboardButton("Конец работы", callback_data='end_work')],
        [InlineKeyboardButton("Отработано сегодня", callback_data='today_working')],
        [InlineKeyboardButton("Назад", callback_data='back')],
    ]
    reply_markup = InlineKeyboardMarkup(additional_keyboard)
    await query.edit_message_text(text="Выберите опцию:", reply_markup=reply_markup)


# Запись статистики в файл JSON
async def write_to_csv(data: dict, file_path=file_path) -> None:
    headers = data.keys()

    with open(file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        if os.path.exists(file_path):
            writer.writerow(data)
        else:
            writer.writeheader()
            writer.writerow(data)
    write_log(message="Статистика Pomodoro записана в файл pomodoro_stats.json.")


async def time_work_func(type_work):
    timestamp = datetime.now().isoformat()
    timestamps = {'job_number': 1, 'type': f'{type_work}', 'timestamp': timestamp}
    await write_to_csv(data=timestamps)

async def get_today_data():
    df = pd.read_csv(
        file_path,
        names=['job_number', 'type', 'timestamp'],
        parse_dates=["timestamp"]
        )
    today_dt = datetime.today().date().strftime('%Y-%m-%d')
    df = df[df['timestamp'] >= today_dt].sort_values(['timestamp'])
    return df


async def get_today_last_event():
    df = await get_today_data()
    last_event = df['type'].iloc[-1]
    return last_event

async def get_today_working_hours():
    df = await get_today_data()

    df['next_timestsamp'] = df['timestamp'].shift(1)
    df = df[df['type'] == 'end_work'].copy()
    df['diff_timestamp'] = (df['timestamp'] - df['next_timestsamp']) / pd.Timedelta(hours=1) # type: ignore
    working_hours = df['diff_timestamp'].sum()
    return int(working_hours), int((working_hours % 1) * 60)
