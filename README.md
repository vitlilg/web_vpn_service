# web_vpn_service
**Проект "Vpn Service"** - простенький vpn сервіс, який буде виглядати як простий веб сайт.
Принцип роботи (опис замовника):
1. Клієнт реєструється на сайті і отримує доступ до особистого кабінету.
2. В особистому кабінеті в нього є редагування якихось своїх особистих даних та розділ статистики де виводиться така інформація:
* кількість переходів між сторінками розділена по сайтах які використовувались через vpn;
*	Об'єм даних який було відправлено і завантажено також по сайтах.
3. Також є розділ де клієнт створює сайти. Сайт це структура яка складається з урл і назви. Таких клієнт може створити безліч.
4. Після створення сайту клієнт може натиснути на кнопку перейти на сайт, але він переходить не на урл цього сайту, а на внутрішній роут, який в свою чергу виступає як проксі сервер до урл сайту на який клієнт хоче перейти.
*Примітка:* якщо користувач натисне на посилання, яке веде на зовнішній ресурс, то він повинен просто перейти на нього. При цьому клієнт залишає наш vpn-вебсайт.

## Стек технологій
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-5.0.1-28a745)
![DRF](https://img.shields.io/badge/DRF-3.14.0-dc3545)
![Celery](https://img.shields.io/badge/Celery-5.3.6-green)
![Postgres](https://img.shields.io/badge/Postgres-14.9-blue)
![Redis](https://img.shields.io/badge/Redis-5.0.1-dc3545)

Повний перелік залежностей - [requirements.txt](./requirements.txt)

## Бази данних
### Postgres
| Назва БД |        Опис        | Версія |
|----------|--------------------|--------|
| default  | Основна база даних | 14.9   |

### Redis
| Номер БД |          Опис         | Версія |
|----------|-----------------------|--------|
|    /3    |   CELERY_BROKER_URL   | 5.0.1  |
|    /4    | CELERY_RESULT_BACKEND | 5.0.1 |

# Запуск проекту
## Змінні оточення
Мінімальні вимоги для запуску проекту
```bash
# Filename: .env

SECRET_KEY=<str>
DEBUG=<bool>

POSTGRES_HOST=<str>
POSTGRES_DB=<str>
POSTGRES_USER=<str>
POSTGRES_PASSWORD=<str>
POSTGRES_DB_PORT=<int>

HOST_API_DOMAIN=<str>
```

Повний перелік змінних оточення - [.env.example](./.env.example)

## Налаштування оточення
Створіть та активуйте віртуальне оточення
```bash
python -m venv venv
source ./venv/bin/activate
```

Активуйте pre-commit
```bash
pre-commit install
```

Зробіть міграцію бази даних
```bash
python manage.py migrate
```

## Celery
Для відкладених завдань запустіть сервіс celery worker
```bash
celery -A web_vpn_service worker --loglevel=INFO
```

## Docker
Для запуску контейнера необхідно створити в корені проекту файл .docker.env на основі цього файлу [.docker.env.example](./.docker.env.example)
У файлі docker-compose.yml у строці *image: vitlilg/web_vpn_service:latest* замість vitlilg вставити назву свого облікового запису для docker.
Потім виконати:
```bash
docker compose build
docker compose up
```
