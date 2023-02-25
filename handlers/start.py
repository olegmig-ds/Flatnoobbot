from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from keyboards.keyboards import select_type_housing


@dp.message_handler(CommandStart())
@dp.callback_query_handler(Text('start'))
async def start(message: types.Message, state: FSMContext):
    '''Запуск бота'''
    state_data = await state.get_data()
    user_selection = state_data.get('type_housing', '')

    if user_selection:
        msg_text = (
            '<b>Выберите тип жилья или нажмите "Дальше ▶":</b>'
        )
    else:
        msg_text = (
            '<b>Выберите тип жилья:</b>'
        )

    if 'data' in message:
        call = message
        await call.message.edit_text(msg_text,
            reply_markup=await select_type_housing(user_selection))
    else:
        state_data = {
            'type_housing': [],
            'room': [],
        }
        await state.update_data(**state_data)

        await message.answer(msg_text,
            reply_markup=await select_type_housing())
