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

kbind = InlineKeyboardBuilder()
yes_button = InlineKeyboardButton(text='Да✅', callback_data='yes-ind')
no_button = InlineKeyboardButton(text='Нет🚫', callback_data='no-ind')
kbind.add(yes_button, no_button)
kbind = kbind.as_markup()


kbdep = InlineKeyboardBuilder()
yes_button = InlineKeyboardButton(text='Да✅', callback_data='yes-dep')
no_button = InlineKeyboardButton(text='Нет🚫', callback_data='no-dep')
kbdep.add(yes_button, no_button)
kbdep = kbdep.as_markup()
