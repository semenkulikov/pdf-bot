# Асинхронный телеграм-бот для генерации PDF-файлов с возможностью подписки и выбора шаблонов

## Описание проекта:
Телеграм-бот, который позволяет пользователям генерировать PDF-файлы с помощью различных шаблонов.

Пользователи могут выбирать шаблоны для различных типов документов (например, подтверждения заказа, верификация аккаунта, товарные квитанции).

Реализовано подключение к платёжной системе для оплаты за генерацию PDF-файлов.

Реализована возможность подписки на премиум тарифы с бонусами для пользователей (например, скидки на генерацию или доступ к дополнительным шаблонам).

## Основной функционал:
* Простой интерфейс для ввода текста, загрузки фото и выбора шаблонов.
* Генерация PDF в зависимости от выбранных параметров (имя магазина, логотип, ссылка для верификации и т.д.).
* Подключение платёжных систем для обработки платежей.
* Админка для управления пользователями, статистикой и шаблонами.
* Система тарифов и подписок.

### Функционал для пользователей:
* Возможность выбора шаблона.
* Генерация одного PDF за 0.2$ или по подписке.
* Интерактивные кнопки в PDF (например, кнопка для перехода на страницу с подтверждением).

## Технические требования:
* Использование Python для разработки бота (aiogram).
* Подключение к API платёжной системы для обработки транзакций.
* Поддержка форматирования текста, шрифтов, цветов и изображений в PDF.

## Требования к безопасности:
* Защита от взлома и спама.

## Стек
* Python 3.13
* Aiogram
* SQLAlchemy
* Alembic
* aiosqlite
* python-dotenv
