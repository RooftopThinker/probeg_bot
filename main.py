import asyncio
import logging
from asyncio import WindowsSelectorEventLoopPolicy
# from aiogram.fsm.storage.redis import RedisStorage ##TODO UNCOMMENT
from aiogram import Bot, Dispatcher
from setup_dispatcher import setup_dispatcher
import config
import aiofiles
from data.database import SqlAlchemyBase, engine
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
dp = Dispatcher()


async def create_metadata():
    async with engine.begin() as conn:
        await conn.run_sync(SqlAlchemyBase.metadata.create_all)


async def main():
    await setup_dispatcher(dp)
    await dp.start_polling(bot, polling_timeout=30)

if __name__ == "__main__":
    asyncio.run(create_metadata())
    asyncio.run(main())

