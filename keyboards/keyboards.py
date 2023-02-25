from aiogram import types


async def get_inline_keyboard(buttons_list, row_width=1):
    '''Возвращает inline-клавиатуру'''
    keyboard = types.InlineKeyboardMarkup(row_width=row_width)

    for buttons in buttons_list:
        keyboard.add(*buttons)

    return keyboard


async def select_type_housing(user_selection=''):
    '''Кнопки для выбора типа жилья'''
    type_housing = {
        'Новостройка': 'type_new',
        'Вторичка': 'type_second',
    }
    buttons = [[]]

    for b_name, b_callback in type_housing.items():
        if b_name in user_selection:
            b_name = '✅ ' + b_name

        buttons[0].append(
            types.InlineKeyboardButton(b_name, callback_data=b_callback)
        )

    if user_selection:
        buttons.append(
            [
                types.InlineKeyboardButton('Дальше ▶',
                    callback_data='room_')
            ]
        )

    return await get_inline_keyboard(buttons, row_width=2)


async def select_number_rooms(user_selection=''):
    '''Кнопки для выбора кол-ва комнат'''
    number_rooms = ['1', '2', '3', '4+', 'студия']
    buttons = [
        [],
        [
            types.InlineKeyboardButton('◀ Назад', callback_data='start')
        ]
    ]

    for n_room in number_rooms:
        if n_room in user_selection:
            b_name = '✅ ' + n_room
        else:
            b_name = n_room

        buttons[0].append(
            types.InlineKeyboardButton(b_name, callback_data=f'room_{n_room}')
        )

    if user_selection:
        buttons[1].append(
            types.InlineKeyboardButton('Дальше ▶', callback_data='req_area')
        )

    return await get_inline_keyboard(buttons, row_width=2)


async def back_button(callback):
    '''Возвращает кнопку "Назад"'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton('◀ Назад', callback_data=callback)
    )

    return keyboard