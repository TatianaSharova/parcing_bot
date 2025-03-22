from aiogram import Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart

from keyboards import reply

user_router = Router()


@user_router.message(CommandStart())
async def send_welcome(message: types.Message) -> types.Message:
    await message.answer(
        'Привет!\n'
        '\n'
        'Чтобы добавить сайты по продажам зюзюбликов для парсинга, '
        'нажми на кнопку "Загрузить файл".',
        parse_mode=ParseMode.HTML,
        reply_markup=reply.get_file
        )
