# **Parcing telegram bot**

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/)
![SQLite](https://a11ybadges.com/badge?logo=sqlite)

Телеграм бот, который предоставляет пользователю возможность добавлять в бд новые сайты для парсинга путем отправки боту exel-файла с данными сайта.

Стек: aiogram, SQLalchemy, telegram, SQLite, python, pandas

## Возможности бота:
1. Валидирует полученный файл: если пользователь прислал файл неверного формата (принимает только xlsx, xls), присылает пользователю сообщение об этом.

2. Присылает пользователю информационное сообщение с данными из файла.

3. Если при создании новых записей в бд произойдет ошибка, пользователь получит сообщение с информацией об ошибке. Например, если какое-то поле оказалось пустым или если url из присланного файла уже есть в базе данных.

4. Сообщает сколько новых сайтов были добавлены в бд после обработки файла.

5. Удаляет файл пользователя после его обработки.


### Локальный запуск бота:

**_Склонировать репозиторий к себе_**
```
git clone git@github.com:TatianaSharova/parcing_bot.git
```
**_В директории проекта создать файл .env и заполнить своими данными:_**       
За основу возьмите файл .env.example
       
**_Создать и активировать виртуальное окружение:_**

Для Linux/macOS:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Для Windows:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
**_Установить зависимости из файла requirements.txt:_**
```
pip install -r requirements.txt
```
**_Запустить бот:_**
```
python bot.py
```

### Как пользоваться:
Пользователь открывает тг бот, нажимает кнопку загрузить файл, отправляет файл формата .xlsx или .xls, в котором заполнены столбцы title, url, xpath

### Автор
[Татьяна Шарова](https://github.com/TatianaSharova)