# Telegram бот

Цей проєкт реалізує тестове завдання, суть в якому реалізувати парсер кількості вакансій на сайті robota.ua та доставити статистику за сьогодні в телеграм у вигляді таблиці

/start - привітання
/help - опис команд
/get_today_statistics - отримання файлу зі статискою на сьогодні.

## Встановлення

Переконайтеся, що у вас встановлено Python версії 3.x.

1. Склонуйте цей репозиторій:

    ```bash
    git clone https://github.com/Anton293/tg-bot.git
    cd tg-bot
    ```
    ##### або завантажте zip архів та розпакуйте, замість git clone ...

2. Встановіть необхідні залежності з файлу `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## Налаштування

Перш ніж запускати програму, вам потрібно отримати токен вашого Telegram бота.

1. Зареєструйте нового бота через [@BotFather](https://t.me/BotFather) в Telegram.
2. Отримайте токен вашого бота.
3. Встановіть змінну середовища `TELEGRAM_BOT_TOKEN` з вашим токеном. Наприклад:

    ```bash
    export TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН
    ```

   Або використовуйте безпосередньо при запуску:

    ```bash
    TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН python3 app.py
    ```

## Запуск

1. Запустіть ваш додаток за допомогою Python:

    ```bash
    export TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН
    python3 app.py
    ```

   Або використовуйте токен при запуску:

    ```bash
    TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН python3 app.py
    ```



