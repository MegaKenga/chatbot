from config import TOKEN_API
from aiogram import Dispatcher, executor, Bot, types
from stickers import *


bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


HELP_COMMANDS = """
/Get_love_sticker - получить милый стикер 

"""
async def on_startup(_):
    print('It is alive!!')

@dp.message_handler(commands = ['start'])
async def start_chat(message: types.Message):
    await message.answer('Смотри, что я умею!')
    await bot.send_message(chat_id=message.chat.id,
                            text = HELP_COMMANDS)

@dp.message_handler(commands = ['Get_love_sticker'])
async def send_sticker(message: types.Message):
    await message.answer(text = 'Смотри какая прелесть!')
    await bot.send_sticker(chat_id = message.chat.id,
                            sticker = random_love_sticker())

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply('Прости, я тебя не понимаю. Для начала работы напиши /start.')

@dp.message_handler(content_types=types.ContentType.STICKER)
async def echo(message: types.Message):
    await message.reply('Прости, я тебя не понимаю. Для начала работы напиши /start.')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup = on_startup, skip_updates=True)