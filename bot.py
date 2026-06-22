import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1003960873649 # Твой ID
WEBAPP_URL = "https://flaafix.github.io/AetrisVPN-MiniApp/"

session = AiohttpSession(timeout=60)
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    try:
        # Проверяем статус в канале
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🚀 Открыть AetrisVPN", web_app=WebAppInfo(url=WEBAPP_URL))]
            ])
            await message.answer("Добро пожаловать! Нажми кнопку ниже для получения ссылки:", reply_markup=markup)
        else:
            await message.answer("❌ Сначала подпишись на наш канал!")
    except Exception:
        await message.answer("⚠️ Ошибка: я не могу проверить подписку. Убедись, что я добавлен в администраторы канала.")

# Веб-заглушка для Render
async def web_server(request): return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", web_server)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
    await site.start()

async def main():
    await asyncio.gather(dp.start_polling(bot), start_web_server())

if __name__ == "__main__":
    asyncio.run(main())
