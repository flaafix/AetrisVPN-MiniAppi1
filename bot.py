import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1003960873649 # <-- СЮДА ВПИШИ ID СВОЕГО КАНАЛА (с минусом!)
WEBAPP_URL = "https://flaafix.github.io/AetrisVPN-MiniApp/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🚀 Открыть AetrisVPN", web_app=WebAppInfo(url=WEBAPP_URL))]
            ])
            await message.answer("Добро пожаловать! Нажми кнопку ниже:", reply_markup=markup)
        else:
            await message.answer("Сначала подпишись на наш канал!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get('/', handle)

# И в конце своего кода перед запуском, вместо простого запуска, 
# нужно запустить и бота, и веб-сервер. 
# Если хочешь, я напишу, как это правильно объединить.
