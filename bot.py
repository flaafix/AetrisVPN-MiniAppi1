import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import web

# Настройка
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1003960873649  # Твой ID канала
CHANNEL_URL = "https://t.me/AetrisVPN" # Ссылка на канал
WEBAPP_URL = "https://flaafix.github.io/AetrisVPN-MiniApp/"

session = AiohttpSession(timeout=60)
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@dp.message(Command("start"))
async def start(message: types.Message):
    if await is_subscribed(message.from_user.id):
        # Если подписан — даем кнопку на WebApp
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Открыть AetrisVPN", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
        await message.answer("Добро пожаловать! Нажми кнопку ниже:", reply_markup=markup)
    else:
        # Если НЕ подписан — даем кнопку «Подписаться»
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")]
        ])
        await message.answer("❌ Для доступа к VPN необходимо подписаться на наш канал:", reply_markup=markup)

@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub_callback(callback: types.CallbackQuery):
    if await is_subscribed(callback.from_user.id):
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Открыть AetrisVPN", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
        await callback.message.edit_text("✅ Спасибо за подписку! Теперь доступ открыт:", reply_markup=markup)
    else:
        await callback.answer("❌ Вы еще не подписались!", show_alert=True)

# Веб-сервер для стабильности Rende
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
