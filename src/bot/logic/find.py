from aiogram import Router, types
from src.bot.Background.QA import search


find_router = Router(name='find')


@find_router.message()
async def find_handler(message: types.Message):
    msg = await message.answer('Здравствуйте! Спасибо за ваш запрос. Я начну поиск контактов по вашему запросу, это может занять некоторое время')
    answer = search(message.text)
    await msg.edit_text("По вашему запросы ничего не найдено. Пожалуйста, проверьте правильность введенной вами информации. Если все введено верно, то попробуйте написать запрос по-другому." if len(answer) == 0 else f"Найдено {len(answer)} контактов:\n{'\n'.join(answer)}")