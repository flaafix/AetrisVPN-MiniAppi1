import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import web

# 1. Настройки (Замени CHANNEL_ID на свой, обязательно с минусом в начале)
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1003960873649 
WEBAPP_URL = "https://flaafix.github.io/AetrisVPN-MiniApp/"

# 2. Инициализация
session = AiohttpSession(timeout=60)
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

# 3. Функция проверки подписки
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Статусы, которые считаются подпиской
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False

# 4. Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    if await is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Открыть AetrisVPN", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
        await message.answer("Добро пожаловать! Нажми кнопку ниже:", reply_markup=markup)
    else:
        await message.answer("❌ **Доступ закрыт!**\n\nЧтобы получить доступ к VPN, подпишись на наш канал и нажми /start снова.")

# 5. Веб-сервер для стабильности (чтобы Render не «усыплял» бота)
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
