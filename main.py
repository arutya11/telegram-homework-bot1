import asyncio
import pandas as pd
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Твой токен бота
TOKEN = "7818847155:AAGB0ztfC7esYnq_fRTwe5z6wiCM-uK--J0"

# ID таблицы (из ссылки)
SHEET_ID = "1yB5oKY9Sqj_VfR39Kp7EOESK7QA4Eig7YxeHUrCDUJs"

# Ссылка на CSV-версию Google Таблицы
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# Функция загрузки данных из Google Sheets
def get_homework(day):
    df = pd.read_csv(CSV_URL)
    df.columns = ["День", "Задание"]  # Указываем названия колонок
    homework = df[df["День"] == day]["Задание"]
    return homework.values[0] if not homework.empty else "Нет заданий на этот день."

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ Новый формат клавиатуры (правильный)
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Понедельник")],
        [KeyboardButton(text="Вторник")],
        [KeyboardButton(text="Среда")],
        [KeyboardButton(text="Четверг")],
        [KeyboardButton(text="Пятница")],
        [KeyboardButton(text="Суббота")],  # Добавили субботу
    ],
    resize_keyboard=True
)

# Обработчик кнопок (обновленный)
@dp.message(F.text.in_(["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]))
async def send_homework(message: types.Message):
    day = message.text
    homework = get_homework(day)
    await message.reply(f"📚 Домашнее задание на {day}:\n{homework}")

# ✅ Новый способ обработки команды /start
@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.reply("Выберите день недели, чтобы узнать домашнее задание:", reply_markup=keyboard)

# Функция для запуска бота
async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
