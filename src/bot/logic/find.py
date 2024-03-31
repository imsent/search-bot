import asyncio

from aiogram import Router, types
from aiogram.filters import CommandStart

find_router = Router(name='find')


@find_router.message()
async def start_handler(message: types.Message):
    msg = await message.answer('Здравствуйте! Спасибо за ваш запрос. Я начну поиск контактов по вашему запросу, это может занять некоторое время')
    await asyncio.sleep(2)
    await msg.edit_text("По вашему запросу ничего не найдено.")