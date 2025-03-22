from aiogram import Bot, F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import reply

from .utils import validate_file

file_router = Router()


# FSM
class AddFile(StatesGroup):

    file = State()


@file_router.message(
        StateFilter(None), Command('add_source'))
@file_router.message(
        StateFilter(None), F.text.strip().lower() == 'загрузить файл')
async def start_getting_file(message: types.Message, state: FSMContext):
    await message.answer(
        'Пришлите exel-файл:',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddFile.file)


@file_router.message(
        StateFilter('*'), Command('cancel'))
@file_router.message(
    StateFilter('*'), or_f(F.text.casefold() == 'отмена',
                           F.text.casefold() == 'cancel'))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(
        'Действия отменены.',
        reply_markup=reply.get_file)


@file_router.message(AddFile.file, F.document)
async def get_file(message: types.Message, state: FSMContext,
                   bot: Bot):
    '''Обрабатывает полученный документ.'''
    file = await bot.get_file(message.document.file_id)

    if await validate_file(file) is False:
        await message.answer(
            'Неподходящий формат. '
            'Пришли файл из слудующих форматов: xlsx, scv.'
        )
        return

    await message.answer(
        '!',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    return


@file_router.message(AddFile.file, F.content_type.not_in({'document', }))
async def get_not_file(message: types.Message, state: FSMContext):
    '''Обрабатывает сообщение неподходящего типа при ожидании документа.'''
    await message.answer(
        'Пришлите exel-файл. Доступные форматы: xlsx, scv. '
        'Если возникла проблема и ты хочешь прерваться, в '
        'меню нажми на команду "Отмена".',
        reply_markup=types.ReplyKeyboardRemove()
    )
    return
