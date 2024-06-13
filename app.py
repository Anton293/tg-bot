import asyncio
import logging
import os
import sqlite3

from parser_module import run_hourly_parse_site

from aiogram import Bot, Dispatcher

from aiogram import types, F, Router
from aiogram.filters import Command


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, filename='logs/telegram_bot.log',
    filemode='w', 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()
router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("1")


@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer("2")


@router.message(Command("get_today_statistics"))
async def get_today_statistics(message: types.Message):
    # ця функція повертає в телеграм статистику за сьогодні, у вигляді excel файлу
    pass


async def strart_telegram_bot():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def main():
    await asyncio.gather(
        run_hourly_parse_site(),
        strart_telegram_bot()
    )


if __name__ == "__main__":
    asyncio.run(main())