# Парсер solscan

## Функциональность
- раз в N минут (конфигурация) получает список ссылок для парсинга из файла ``links.txt``
- по каждой ссылке получает актуальный список транзакций
- отправляет уведомления в telegram по всем новым транзакциям

## Установка
- ``pip install -r requirements.txt``
- ``cp links.txt.examlpe links.txt``, отредактировать
- ``cp config.ini.example config.ini``, отредактировать

## Запуск
``python parser.py``

## Реализация
- ``system/manager`` - LinksManager (основной класс проекта, бизнес логика работы)
- ``system/parser`` - Parser (класс для парсинга страниц)
- ``system/messenger`` - Messenger (singleton, класс для отправки нотификаций)
