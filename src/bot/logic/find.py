from aiogram import Router, types
import aiohttp
from src.configuration import conf

find_router = Router(name='find')


async def url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.json()
            return result


@find_router.message()
async def find_handler(message: types.Message):
    msg = await message.answer(
        "Здравствуйте! Спасибо за ваш запрос. Я начну поиск контактов по вашему запросу, это может занять некоторое время")
    answer = await url(f"http://{conf.host}:8080/search/{message.text}")

    await msg.edit_text(
        "По вашему запросы ничего не найдено. Пожалуйста, проверьте правильность введенной вами информации. Если все введено верно, то попробуйте написать запрос по-другому." if len(
            answer) == 0 else f"Найден сотрудник, соответствующий вашему запросу:\n{'\n'.join(answer['answer'])}")
