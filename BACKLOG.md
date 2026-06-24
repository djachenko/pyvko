# Backlog



## mypy exclusions (нужно вернуть)

- `pyvko/pyvko_runner.py` — исключён через `[[tool.mypy.overrides]] ignore_errors = true` в pyproject.toml. Файл содержит старый демо-код с ~20 реальными ошибками (устаревший API, неверные типы). Нужно либо выпилить файл, либо привести в соответствие с текущим API.
