FROM python:alpine3.17

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.0

WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"

COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi


CMD ["poetry", "run", "python", "./starship/__init__.py"]
EXPOSE 5000
