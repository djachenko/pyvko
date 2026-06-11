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

## Текущее состояние

- Стабильная версия: `0.1.11`
- 39 незакоммиченных файлов — нужна ревизия и актуализация
- VK posting продолжается, upload команда в justin активно используется

---

## Что нужно сделать

- **Актуализировать**: разобрать 39 dirty-файлов, закоммитить актуальное или отбросить
- **Переиспользуемый код** → вынести в `justin_utils` (shared-утилиты которые могут пригодиться за пределами VK-интеграции)
- Upload-команда в justin сложная — если понадобятся изменения в pyvko под неё, смотреть сюда

---

## Git

Semantic commits: `feat:`, `fix:`, `refactor:`, `chore:`
