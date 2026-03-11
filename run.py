from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from fastapi.middleware.cors import CORSMiddleware

TOKEN = "8730984401:AAGohTP7eBoOUpnQhRFoh4pYk-3i6eQyapo"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://lover-service.onrender.com/webhook/{TOKEN}"
MY_TG_ID = 5568565327

bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # разрешаем все
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Команда /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот работает через webhook 🚀")

# Telegram webhook endpoint
@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update = await request.json()
    await dp.feed_raw_update(bot, update)
    return {"ok": True}

# Новый endpoint для пересылки POST запросов в Telegram
@app.post("/send_to_telegram")
async def send_to_telegram(request: Request):
    try:
        data = await request.json()  # пытаемся получить JSON
    except:
        data = await request.body()  # если не JSON, получаем как bytes
        data = data.decode('utf-8')

    # Отправляем данные в Telegram
    await bot.send_message(MY_TG_ID, f"Получен POST запрос:\n{data}")
    return {"status": "ok", "message": "Данные отправлены в Telegram"}