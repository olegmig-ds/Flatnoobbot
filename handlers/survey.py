import shelve

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp
from data import config
from keyboards import keyboards


class SurveyStates(StatesGroup):
    waiting_for_area = State()
    waiting_for_range_price = State()


@dp.callback_query_handler(Text(startswith='type_'), state='*')
async def select_type_housing(call: types.CallbackQuery, state: FSMContext):
    '''Выбор типа жилья'''
    await call.answer()
    await state.reset_state(with_data=False)
    state_data = await state.get_data()
    type_housing = call.data.split('_')[-1]
    user_selection = state_data['type_housing']

    if type_housing == 'new':
        type_housing = 'Новостройка'
    elif type_housing == 'second':
        type_housing = 'Вторичка'

    if type_housing not in state_data['type_housing']:
        user_selection.append(type_housing)
    else:
        user_selection.remove(type_housing)

    state_data['type_housing'] = user_selection
    await state.update_data(**state_data)

    if user_selection:
        msg_text = (
            '<b>Выберите тип жилья или нажмите "Дальше ▶"</b>'
        )
    else:
        msg_text = (
            '<b>Выберите тип жилья:</b>'
        )

    await call.message.edit_text(msg_text,
        reply_markup=await keyboards.select_type_housing(user_selection))


@dp.callback_query_handler(Text(startswith='room_'), state='*')
async def select_number_room(call: types.CallbackQuery, state: FSMContext):
    '''Выбор кол-ва комнат'''
    await state.reset_state(with_data=False)
    state_data = await state.get_data()
    user_selection = state_data['room']
    room = call.data.split('_')[-1]

    if room != '' and room not in user_selection:
        user_selection.append(room)
    elif room in user_selection:
        user_selection.remove(room)

    state_data['room'] = user_selection
    await state.update_data(**state_data)

    if user_selection:
        msg_text = ('<b>Выберите кол-во комнат или нажмите "Дальше ▶"</b>')
    else:
        msg_text = ('<b>Выберите кол-во комнат:</b>')

    await call.message.edit_text(msg_text,
        reply_markup=await keyboards.select_number_rooms(user_selection))


@dp.callback_query_handler(Text('req_area'), state='*')
async def req_area(call: types.CallbackQuery, state: FSMContext):
    '''Запрос площади'''
    await call.answer()

    msg_text = (
        '<b>Отправьте площадь жилья:</b>'
    )
    keyboard = await keyboards.back_button(f'room_')

    await call.message.edit_text(msg_text, reply_markup=keyboard)
    await SurveyStates.waiting_for_area.set()


@dp.message_handler(state=SurveyStates.waiting_for_area)
async def req_price_range(message: types.Message, state: FSMContext):
    '''Сохраняет площадь жилья и запрашивает диапазон цен'''
    state_data = await state.get_data()
    area = [i for i in message.text if i.isdigit()]

    if area:
        area = int(''.join(area))
        await state.update_data(area=area)

        msg_text = (
            '<b>Отправьте диапазон цен в формате:</b> <code>цена - цена</code>'
        )
        keyboard = await keyboards.back_button(f'req_area')

        await message.answer(msg_text, reply_markup=keyboard)
        await state.reset_state(with_data=False)
        await SurveyStates.waiting_for_range_price.set()
    else:
        msg_text = (
            '<b>Площадь жилья должна включать цифры!</b>'
        )
        await message.answer(msg_text)


@dp.message_handler(state=SurveyStates.waiting_for_range_price)
async def save_survey_data(message: types.Message, state: FSMContext):
    '''Сохранение данных опроса в виде словаря в бинарный файл'''
    user_id = message.from_user.id
    range_price = message.text.replace(' ', '').split('-')

    if len(range_price) == 2:
        price_from = int(''.join([i for i in range_price[0] if i.isdigit()]))
        price_to = int(''.join([i for i in range_price[1] if i.isdigit()]))
        range_price = f'{price_from} - {price_to}'

        state_data = await state.get_data()
        survey_data = {
            'Тип жилья': state_data['type_housing'],
            'Количество комнат': state_data['room'],
            'Площадь': state_data['area'],
            'Диапазон цен': range_price,
        }
        print(survey_data)

        with shelve.open('survey.data') as file:
            file[str(user_id)] = survey_data

        msg_text = (
            '<b>Данные опроса сохранены!</b>'
        )

        await message.answer(msg_text)
        await state.reset_state()

        # Отправка данных опроса администраторам
        for admin_id in config.ADMINS:
            admin_msg = str(survey_data)
            admin_msg += (
                '\n\nТакже данные сохранены в файл survey.data '
                f'под ключом "{user_id}"!'
            )
            await dp.bot.send_message(admin_id, admin_msg)
    else:
        msg_text = (
            '<b>Отправьте диапазон в формате:</b> <code>цена - цена</code>'
        )
        await message.answer(msg_text)