from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

kb = InlineKeyboardBuilder()
yes_button = InlineKeyboardButton(text='Да✅', callback_data='yes')
no_button = InlineKeyboardButton(text='Нет🚫', callback_data='no')
kb.add(yes_button, no_button)
kb = kb.as_markup()

kb2 = InlineKeyboardBuilder()
no_button = InlineKeyboardButton(text='Отмена🚫', callback_data='cancel')
kb2.add(no_button)
kb2 = kb2.as_markup()

kb3 = InlineKeyboardBuilder()
yes_button = InlineKeyboardButton(text='Да✅', callback_data='show')
kb3.add(yes_button)
kb3 = kb3.as_markup()

