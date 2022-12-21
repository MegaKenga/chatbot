from config import TOKEN_API
from aiogram import Dispatcher, executor, Bot, types
from stickers import *
import random
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
ATTEMPTS = 5
users: dict = {}

def get_random_number() -> int:
    return random.randint(1, 10)


HELP_COMMANDS = """
/get_love_sticker - получить миленький стикер 
/play_game - начать веселую игру!
/help - получить помощь и узнать правила игры

"""
async def on_startup(_):
    print('It is alive!!')

@dp.message_handler(commands = ['start'])
async def start_chat(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}

        if not users[message.from_user.id]['in_game']:
            await message.answer('Смотри, что я умею!')
            await bot.send_message(chat_id=message.chat.id,
                                    text = HELP_COMMANDS)
        else:
            await message.answer ('Пока мы играем в игру я могу реагировать только на числа от 1 до 10 и команды /cancel и /stat')

@dp.message_handler(commands = ['cancel'])
async def cancel_game(message: Message):
    users[message.from_user.id]['in_game'] = False
    await message.answer("""/get_love_sticker - получить миленький стикер 
/play_game - начать веселую игру!
/help - получить помощь и узнать правила игры""")

@dp.message_handler(commands = ['get_love_sticker'])
async def send_sticker(message: Message):
    if not users['in_game']:
        await message.answer(text = 'Смотри какая прелесть!')
        await bot.send_sticker(chat_id = message.chat.id,
                                sticker = random_love_sticker())
    else:
        await message.answer ('Пока мы играем в игру я могу реагировать только на числа от 1 до 10 и команды /cancel и /stat.')

@dp.message_handler(commands = ['help'])
async def send_help(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(text = 'Этот бот создан, чтобы поднять тебе настроение и немного поиграть в угадайку.'
        'Команда /get_love_sticker пришлет тебе миленький стикер, а команда /play_game запустит игру в угадайку.'
        'Чтобы узнать правила игры, набери /rules')
    else:
        await message.answer ('Пока мы играем в игру я могу реагировать только на числа от 1 до 10 и команды /cancel и /stat')

@dp.message_handler(commands = ['rules'])
async def send_rules(message: Message):
    await message.answer(text = f'Правила игры:\n\nЯ загадываю число от 1 до 10, а вам нужно его угадать\nУ вас есть {ATTEMPTS} попыток')

@dp.message_handler(commands = ['play_game'])
async def play_the_game(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(text = f'Ура! Итак, я загадал число от одного до 10. Ты должен отгадать его за {ATTEMPTS} попыток.')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = 0
    else:
        await message.answer('Пока мы играем в игру я могу реагировать только на числа от 1 до 10 и команды /cancel и /stat')

@dp.message_handler(lambda message: message.text.isdigit() and 1 <= int(message.text) <= 10)
async def user_play_game(message: Message):
    if users[message.from_user.id]['in_game'] == True:
        if int(message.text) == users [message.from_user.id] ['secret_number']:
            users[message.from_user.id]['attempts'] += 1
            await message.answer(text = f'Молодец, ты отгадал число за {users[message.from_user.id]["attempts"]} попыток.')
            users[message.from_user.id]['in_game'] = False
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer(text = 'Мое число меньше.')
            users[message.from_user.id]['attempts'] += 1
        elif int(message.text) < int(users[message.from_user.id]['secret_number']):
            await message.answer(text = 'Мое число больше.')
            users[message.from_user.id]['attempts'] += 1
        if users[message.from_user.id]['attempts'] == ATTEMPTS:
            await message.answer(f'К сожалению, у вас больше не осталось попыток. Вы проиграли :(\n\nМое число было {users["secret_number"]}\n\nЧтобы сыграть еще раз выберите /play_game')
            users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('Прости, я тебя не понимаю. Для начала работы напиши /start.')
        
@dp.message_handler()
async def wrong_answer(message: Message):
    if users[message.from_user.id]['in_game'] == True:
        await message.answer('Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 10.')
    else:
        await message.reply('Прости, я тебя не понимаю. Для начала работы напиши /start.')

@dp.message_handler(content_types=types.ContentType.STICKER)
async def echo(message: Message):
    await message.reply('Прости, я тебя не понимаю. Для начала работы напиши /start.')

@dp.message_handler(content_types=types.message)
async def echo(message: Message):
    await message.reply('Прости, я тебя не понимаю. Для начала работы напиши /start.')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup = on_startup, skip_updates=True)