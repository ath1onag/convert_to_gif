import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers import handlers
from config_data.config import Config, load_config
from database.database import create_table

logging.basicConfig(level=logging.INFO)


async def main():
    # Создаем таблицу, если она не существует
    await create_table()

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(handlers.router)


    async def set_main_menu(bot: Bot):
        # Создаем список с командами и их описанием для кнопки menu
        main_menu_commands = [
            BotCommand(command='/start',
                       description='Запуск бота'),
            BotCommand(command='/help',
                       description='Справка по работе бота'),
        ]

        await bot.set_my_commands(main_menu_commands)

        # Регистрируем асинхронную функцию в диспетчере,
        # которая будет выполняться на старте бота,
        await dp.startup.register(set_main_menu)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())

