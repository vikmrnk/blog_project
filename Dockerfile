FROM python:3.11-slim

WORKDIR /app

# Встановлюємо Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && mv /root/.local/bin/poetry /usr/local/bin/poetry

# Копіюємо файли Poetry
COPY pyproject.toml poetry.lock ./

# Налаштовуємо Poetry щоб не створювати віртуальне середовище всередині контейнера
RUN poetry config virtualenvs.create false

# Встановлюємо залежності
RUN poetry install --no-interaction --no-root

# Копіюємо решту додатку
COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"] 