import os

POSTGRES_HOST_FALLBACK = "localhost"
POSTGRES_USER_FALLBACK = "root"
POSTGRES_PASSWORD_FALLBACK = "toor"
POSTGRES_DATABASE_FALLBACK = "starship"

POSTGRES_USER = os.getenv("POSTGRES_USER", POSTGRES_USER_FALLBACK)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", POSTGRES_HOST_FALLBACK)
POSTGRES_DATABASE = os.getenv("POSTGRES_DB", POSTGRES_DATABASE_FALLBACK)
POSTGRES_PASSWORD_FILE = os.getenv("POSTGRES_PASSWORD_FILE")


def get_postgres_password():
    if POSTGRES_PASSWORD_FILE:
        with open(POSTGRES_PASSWORD_FILE) as file:
            return file.read().rstrip()
    return POSTGRES_PASSWORD_FALLBACK


def get_url():
    return f"postgresql+psycopg2://{POSTGRES_USER}:{get_postgres_password()}@{POSTGRES_HOST}:5432/{POSTGRES_DATABASE}"
