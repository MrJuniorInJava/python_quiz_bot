import asyncio
import os
import json
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
import nest_asyncio
from bot.handlers import register_handlers  # Assuming you have a register_handlers function
from bot.db import create_table  # Assuming you have a create_table function
from config import API_TOKEN  # Assuming you have a config file with API_TOKEN

nest_asyncio.apply()

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    await create_table()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(base_dir, '..', 'data', 'quiz_data.json')

    with open(json_file_path, 'r', encoding='utf-8') as file:
        quiz_data = json.load(file)

    register_handlers(dp, quiz_data)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
