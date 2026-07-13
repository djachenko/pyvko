# pyvko — Project Guide

## Что это

Типизированная объектно-ориентированная обёртка над `vk_api` для работы с VK API. Часть Python фотоэкосистемы — используется в `justin` для публикации фотосетов.

Написано для личного использования, опубликовано как отдельная библиотека.

---

## Место в экосистеме

```
justin ──→ pyvko ──→ VK API
```

Основной потребитель — команда `upload` в `justin`. Критическая зависимость: без pyvko публикация фото в VK не работает.

---

## Стек

- Python 3.8+, `vk_api`
- Архитектура: mixin-based capabilities (`ApiBased` + аспекты)
- Установка в justin: `pip install -e ../pyvko`

---

## Структура

```
pyvko/
├── pyvko_main.py      # Точка входа: Pyvko(config)
├── api_based.py       # ApiBased, ApiMixin — базовые классы с доступом к api
├── aspects/           # Mixin-возможности: posts, albums, events, groups, likes...
├── entities/          # user.py
├── config/            # Config.read(path) — читает access_token из json
└── shared/            # Throttler, utils
```

**Аспекты** — это mixin-классы которые добавляют возможности группам/пользователям:
`Posts`, `Albums`, `Events`, `Groups`, `Likes`, `Reposts`, `Comments`

---

## Status

- **Состояние:** active
- **Последнее** — исправлены KeyError на optional полях VK API (online, screen_name, start_date, is_closed); настроен pytest-dotenv для токенов через .env (2026-07-12)
- **Следующее** — реализовать progress-tracking (src/pyvko/shared/progress_file.py); реализовать `video.save` upload; отвязаться от `vk_api`; удалить `Throttler`
- **Блокеры** — —

---

## Текущее состояние

- Стабильная версия: `0.1.13`
- VK posting продолжается, upload команда в justin активно используется
- Зависимость от `vk_api` — запланировано убрать (бэклог)

---

## Что нужно сделать

- **Отвязаться от vk_api** → скопировать session/proxy/upload/exceptions в `src/pyvko/vk/`
- **Актуализировать**: разобрать dirty-файлы на ветке `test/integration`, закоммитить актуальное или отбросить
- **Переиспользуемый код** → вынести в `justin_utils` (shared-утилиты которые могут пригодиться за пределами VK-интеграции)
- Upload-команда в justin сложная — если понадобятся изменения в pyvko под неё, смотреть сюда

---

## Git

Semantic commits: `feat:`, `fix:`, `refactor:`, `chore:`
