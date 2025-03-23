from aiogram import types
from pandas import Series
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Source
from logger import logging


async def orm_add_source(session: AsyncSession,
                         row: Series, message: types.Message) -> bool:
    '''
    Создание новой записи с обработкой возможных исключений.
    Если возникнет ошибка, пользователю придет уведомление.
    '''
    mess = None

    try:
        obj = Source(
            title=row['title'],
            url=row['url'],
            xpath=row['xpath']
            )
        session.add(obj)
        await session.commit()
        return True
    except IntegrityError as e:
        await session.rollback()
        if 'UNIQUE constraint failed' in str(e):
            mess = f'Дубликат URL: {row["url"]} уже есть в базе.'
            logging.warning(f'{mess}: {e}')
        else:
            mess = (f'Ошибка при обработке данных {row["url"]}: возможно, '
                    f'слишком длинное название или наличие пустых полей. '
                    f'Проверьте введенные данные.')
            logging.error(f'Ошибка целостности данных: {e}')
    except DataError as e:
        await session.rollback()
        mess = ('Ошибка длины строки или формата данных. '
                'Проверьте введенные данные.')
        logging.error(f'Ошибка длины строки или формата данных: {e}')
    except Exception as e:
        await session.rollback()
        mess = 'Ошибка. Попробуйте позже.'
        logging.error(f'Ошибка: {e}')

    if mess:
        await message.answer(mess)
        return False
