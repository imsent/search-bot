from aiogram import Router, types
import aiohttp
from aiogram.fsm.context import FSMContext

from bot.configuration import conf
from bot.src.keyboards import *
from aiogram import F

find_router = Router(name='find')

user_storage = {}


async def url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.json()
            return result


@find_router.message(F.text)
async def find_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer_text = message.text.replace('?', '')
    state_now = await state.get_state()
    user_storage[message.from_user.id] = []
    if state_now == 'many':
        await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['extra'])
    if state_now is not None:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=data['id'])
    if state_now == 'correction':
        answer_text = data["text"] + ' ' + answer_text
    msg = await message.answer(
        "Начинаю поиск контактов по вашему запросу, это может занять некоторое время")
    if 'text' in data.keys() and state_now == 'correction':
        answer = await url(f"http://{conf.host}:8080/search/{answer_text}/{message.from_user.id}/yes")
    else:
        answer = await url(f"http://{conf.host}:8080/search/{answer_text}/{message.from_user.id}")
    await state.clear()
    answer = answer['answer']
    if not answer:
        await msg.edit_text("Ничего не найдено")
    else:
        await msg.edit_text(
            f"Найдены сотрудники, соответствующие вашему запросу:")

        for x in answer[:10]:
            await message.answer(
                f'{x['name']}           {x['id']}\n✉️ {x["mail"]}\nТел: {x["number"]}\nКомпания: {x["company"]}\nДолжность: {x["post_dep"]}\nПодразделение: {x["industry"]}\nФункции: {x['funcs']}')
        await state.set_state("output_results")
        if len(answer) > 10:
            await state.set_state('many')
            for x in answer[10:]:
                user_storage[message.from_user.id].append(f'{x['name']}           {x['id']}\n✉️ {x["mail"]}\nТел: {x["number"]}\nКомпания: {x["company"]}\nДолжность: {x["post_dep"]}\nПодразделение: {x["industry"]}\nФункции: {x['funcs']}')
            ext = await message.answer(f"Найдено еще {len(user_storage[message.from_user.id])} сотрудников. Показать?", reply_markup=kb3)
            await state.update_data(extra=ext.message_id)
        msg = await message.answer(text="Нашли ли вы необходимого сотрудника?", reply_markup=kb)
    await state.update_data(text=answer_text, id=msg.message_id)


@find_router.callback_query(F.data == 'cancel')
@find_router.callback_query(F.data == 'yes')
async def delete_message(callback: types.CallbackQuery, state: FSMContext):
    st = await state.get_state()
    if st == 'many':
        data = await state.get_data()
        await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=data['extra'])
    await state.clear()
    await callback.message.delete()


@find_router.callback_query(F.data == 'no')
async def clarify_search(callback: types.CallbackQuery, state: FSMContext):
    st = await state.get_state()
    if st == 'many':
        data = await state.get_data()
        await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=data['extra'])
    await state.set_state("correction")
    await callback.message.edit_text(text='Добавьте уточнение запросу:', reply_markup=kb2)


@find_router.callback_query(F.data == 'show')
async def clarify_search(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state("output_results")
    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=data['extra'])
    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=data['id'])
    for x in user_storage[callback.from_user.id]:
        await callback.message.answer(x)
    msg = await callback.message.answer(text="Нашли ли вы необходимого сотрудника?", reply_markup=kb)
    await state.update_data(id=msg.message_id)


@find_router.message()
async def delete(message: types.Message):
    await message.delete()
