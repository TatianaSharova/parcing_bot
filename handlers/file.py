import os

from aiogram import Bot, F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import reply
from logger import logging

from .utils import download_file, save_source_in_db, validate_file

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
async def handle_file(message: types.Message, state: FSMContext,
                      bot: Bot, session: AsyncSession) -> None:
    '''Обрабатывает полученный документ:
    -проверяет формат файла
    -скачивает файл локально
    -загружает данные из файла в бд
    -уведомляет, сколько сайтов из файла добавлены в бд
    -удаляет скачанный файл
    '''
    file = await bot.get_file(message.document.file_id)

    if await validate_file(file) is False:
        await message.answer(
            'Неподходящий формат. '
            'Пришли файл из следующих форматов: xlsx, xls.'
        )
        return

    file_path = await download_file(file, bot)

    added_count_sources = await save_source_in_db(file_path, session, message)

    if added_count_sources > 0:
        await message.answer(
            f'Добавлено {added_count_sources} новых сайтов в базу.')
    else:
        await message.answer('В базу не были добавлены новые сайты.')

    try:
        os.remove(file_path)
        logging.info(f' Файл {file_path} удален.')
    except PermissionError:
        logging.error(f' Файл {file_path} не удален, занят другим процессом.')
    except Exception as e:
        logging.error(f'Не удалось удалить {file_path}: {e}')

    await state.clear()
    return


@file_router.message(AddFile.file, F.content_type.not_in({'document', }))
async def get_not_file(message: types.Message, state: FSMContext):
    '''Обрабатывает сообщение неподходящего типа при ожидании документа.'''
    await message.answer(
        'Пришли exel-файл. Доступные форматы: xlsx, scv. '
        'Если возникла проблема и ты хочешь прерваться, в '
        'меню нажми на команду "Отмена".',
        reply_markup=types.ReplyKeyboardRemove()
    )
    return
