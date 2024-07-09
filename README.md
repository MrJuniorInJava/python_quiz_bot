# Telegram Quiz Bot

Это Telegram-бот для проведения квизов.

## Команды

`/start` - запуск бота  
`/quiz` - начать квиз  
`/stats` - статистика(выводит последний результат пользователя)

## Установка и запуск

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/ваш_логин/your_repo_name.git
    cd your_repo_name
    ```

2. Создайте виртуальное окружение и установите зависимости:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
3. Откройте файл .env и запишите ваш API_TOKEN: 
    ```
    API_TOKEN=ваш_токен_здесь
    ```

4. Запустите бота:
    ```sh
    python -m bot.main
    ```

## Структура проекта

- `bot/` - Код бота.
- `data/` - Файлы данных.
- `.gitignore` - Файлы и папки, игнорируемые Git.
- `README.md` - Описание проекта.
- `requirements.txt` - Зависимости проекта.
- `config.py` - Конфигурационный файл (если нужен).
