import pandas as pd
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import File, Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.orm_query import orm_add_source
from logger import logging


async def validate_file(file: File) -> bool:
    '''Проверяет формат присланного документа.'''
    formats = ['.xlsx', '.xls']

    for format in formats:
        if format in file.file_path:
            return True
    return False


async def download_file(file: File, bot: Bot) -> str:
    '''Скачивает файл локально в папку /documents'''
    await bot.download_file(file.file_path, file.file_path)
    logging.info(f'Файл успечно скачан локально. '
                 f'Местоположение: {file.file_path}')
    return file.file_path


def format_row(row: pd.Series) -> str:
    '''Форматирует строку в читабельный вид.'''
    title = row.get('title', 'Не указано')
    url = row.get('url', 'Не указано')
    xpath = row.get('xpath', 'Не указано')

    return (
        f'📌 <b>Название:</b> {title}\n'
        f'🔗 <b>Ссылка:</b> {url}\n'
        f'🔍 <b>Путь к цене:</b> {xpath}\n'
    )


def get_text(df: pd.DataFrame) -> str:
    '''Создает сообщение с полученными данными от пользователя.'''
    message_text = 'Файл получен. Вот ваши данные:\n\n'
    message_text += '\n'.join(df.apply(format_row, axis=1))
    message_text += '\n\nПриступаем к загрузке данных в бд.'

    if len(message_text) > 4000:
        message_text = message_text[:4000] + '...\n\n('
        'Слишком много данных, показаны только первые строки)'
    return message_text


async def save_source_in_db(file_path: str,
                            session: AsyncSession,
                            message: Message) -> int:
    '''
    Сохраняет данные из файла в бд,
    а также выводит данные из файла пользователю в сообщении.
    '''
    count = 0

    df = pd.read_excel(file_path)

    file_text = get_text(df.fillna("Не указано"))

    await message.answer(
        file_text,
        parse_mode=ParseMode.HTML,
    )

    for index, row in df.iterrows():
        source = await orm_add_source(session, row, message)
        if source is True:
            count += 1

    return count
