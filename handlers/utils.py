from aiogram.types import File


async def validate_file(file: File) -> bool:
    '''Проверяет формат присланного документа.'''
    formats = ['.xlsx', '.scv']

    for format in formats:
        if format in file.file_path:
            return True
    return False
