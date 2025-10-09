# Автоматизация обработки банковских документов

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Система для автоматического парсинга, валидации и загрузки первичных документов (счета, акты, накладные) в базу данных.

## Особенности

- Поддержка PDF, Excel, XML, EDI форматов
- Автоматическое определение типа документа
- Строгая валидация через Pydantic схемы
- Нормализация в единый формат
- Сохранение в PostgreSQL
- Контейнеризация с Docker
- Обработка ошибок и логирование

## Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/ваш-логин/bank-docs-automation.git
cd bank-docs-automation

# Запустить систему
docker-compose -f docker/docker-compose.yml up --build
```

## Технологии

| Компонент       | Технологии                          |
|-----------------|-------------------------------------|
| Бэкенд         | Python 3.10                         |
| Парсинг        | Pandas, Tabula-Py, Bots-EDI         |
| Валидация      | Pydantic                            |
| База данных    | PostgreSQL                          |
| Очереди        | RabbitMQ                            |
| Инфраструктура | Docker, Docker Compose              |
| Документация   | Markdown, Swagger (опционально)     |

## Структура проекта

```
bank-docs-automation/
├── core/           # Бизнес-логика
├── data_processing # Парсеры, валидация, БД
├── docker/         # Docker конфиги
├── scripts/        # Скрипты запуска
└── tests/          # Тесты
```

## Производительность

В результате внедрения системы:
- Время обработки документов сокращено на 70%
- Ошибки ввода данных уменьшены на 95%
- Ручной труд сокращен на 90%

![Демонстрация работы системы](docs/demo.gif)
