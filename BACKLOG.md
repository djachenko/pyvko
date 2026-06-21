# Backlog

## mypy third-party stubs

`[tool.mypy] ignore_missing_imports = true` — временное решение. `vk_api` не имеет type stubs на PyPI. `requests` имеет (`types-requests`). Нужно:
1. Добавить `types-requests` в test-зависимости
2. Для `vk_api` — написать минимальные inline stubs или добавить точечный override
3. Проработать на уровне repokit CI: `mypy --install-types --non-interactive && mypy src/`



## mypy exclusions (нужно вернуть)

- `pyvko/pyvko_runner.py` — исключён через `[[tool.mypy.overrides]] ignore_errors = true` в pyproject.toml. Файл содержит старый демо-код с ~20 реальными ошибками (устаревший API, неверные типы). Нужно либо выпилить файл, либо привести в соответствие с текущим API.
