from aiogram import executor

import utils, handlers
from loader import dp


async def on_startup(dp):
    '''Действия при запуске бота'''
    print('Бот запущен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)