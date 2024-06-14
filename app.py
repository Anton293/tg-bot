import asyncio
import logging
import os

from parser_module import run_hourly_parse_site
from generator_file_table_xlsx import create_xlsx_table

from aiogram import Bot, Dispatcher

from aiogram import types, F, Router
from aiogram.filters import Command

from datetime import datetime, timedelta


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, 
    filemode="w", 
    filename="bot.log", 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()
router = Router()


last_data_generation_file_xlsx = datetime.now() - timedelta(hours=2)
buffer_document_xlsx = None


@router.message(Command("start"))
async def start(message: types.Message):
    """Send start message."""
    await message.answer("Hello! Use /help to get help.")


@router.message(Command("help"))
async def help(message: types.Message):
    """Send help message."""
    help_message = "/get_today_statistic - get statistics for today. \n/help - get help."
    await message.answer(help_message)


@router.message(Command("get_today_statistic"))
async def get_today_statistic(message: types.Message):
    """Send xlsx file with today statistics."""
    global last_data_generation_file_xlsx, buffer_document_xlsx

    if (datetime.now() - last_data_generation_file_xlsx).seconds > 60*29:
        await create_xlsx_table()
        buffer_document_xlsx = types.FSInputFile("data/vacancies_data.xlsx", filename="Statistics.xlsx")
        last_data_generation_file_xlsx = datetime.now()

    await message.answer_document(buffer_document_xlsx)


async def strart_telegram_bot():
    """Start telegram bot."""
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def main():
    """Run parser and telegram bot."""
    await asyncio.gather(
        run_hourly_parse_site(),
        strart_telegram_bot()
    )


if __name__ == "__main__":
    asyncio.run(main())
