from aiogram import Router, types
import aiohttp
from aiogram.fsm.context import FSMContext

from src.configuration import conf
from src.bot.keyboards import kb, kb2
from aiogram import F

find_router = Router(name='find')


async def url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.json()
            return result


@find_router.message(F.text)
async def find_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    answer_text = message.text
    state_now = await state.get_state()
    if state_now is not None:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data['id'])
    if state_now == 'correction':
        answer_text = data["text"] + ' ' + answer_text + '?'

    msg = await message.answer(
        "Начинаю поиск контактов по вашему запросу, это может занять некоторое время")
    answer = await url(f"http://{conf.host}:8080/search/{answer_text}")
    await state.clear()

    if answer['answer'][0] == "Нет ответа":
        await msg.edit_text(text="Этот вопрос не относится к сотрудникам, задайте другой")
    elif answer['answer'][0] == "Мало информации":
        await state.set_state("correction")
        await state.update_data(text=answer_text.replace('?', ''), id=msg.message_id)
        await msg.edit_text(text="Мало информации, уточните запрос:", reply_markup=kb2)
    else:
        await msg.edit_text(
            f"Найдены сотрудники, соответствующие вашему запросу:")
        for x in answer['answer']:
            await message.answer(
                f'{x['name']}\n✉️ {x["mail"]}\nТел: {x["number"]}\nКомпания: {x["company"]}\nДолжность: {x["post"]}\nПодразделение: {x["industry"]}')
        await state.set_state("output_results")
        msg = await message.answer(text="Нашли ли вы необходимого сотрудника?", reply_markup=kb)
        await state.update_data(text=answer_text.replace('?', ''), id=msg.message_id)


@find_router.callback_query(F.data == 'cancel')
@find_router.callback_query(F.data == 'yes')
async def delete_message(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


@find_router.callback_query(F.data == 'no')
async def clarify_search(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state("correction")
    await callback.message.edit_text(text='Уточните запрос:', reply_markup=kb2)


@find_router.message()
async def delete(message: types.Message):
    await message.delete()

