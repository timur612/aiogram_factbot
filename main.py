import sys

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import config
from handlers import facts, out_of_order, common

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())

    redis = Redis(host="redis")

    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.include_routers(out_of_order.router)
    dp.include_routers(common.router, facts.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
