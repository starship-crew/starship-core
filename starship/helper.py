import os

from urllib.parse import urlparse, urljoin
from flask import request

POSTGRES_HOST_FALLBACK = "localhost"
POSTGRES_USER_FALLBACK = "root"
POSTGRES_PASSWORD_FALLBACK = "toor"
POSTGRES_DATABASE_FALLBACK = "starship"

POSTGRES_USER = os.getenv("POSTGRES_USER", POSTGRES_USER_FALLBACK)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", POSTGRES_HOST_FALLBACK)
POSTGRES_DATABASE = os.getenv("POSTGRES_DB", POSTGRES_DATABASE_FALLBACK)
POSTGRES_PASSWORD_FILE = os.getenv("POSTGRES_PASSWORD_FILE")


def get_db_url():
    def get_postgres_password():
        if POSTGRES_PASSWORD_FILE:
            with open(POSTGRES_PASSWORD_FILE) as file:
                return file.read().rstrip()
        return POSTGRES_PASSWORD_FALLBACK

    return f"postgresql+psycopg2://{POSTGRES_USER}:{get_postgres_password()}@{POSTGRES_HOST}:5432/{POSTGRES_DATABASE}"


def is_safe_url(target):
    """A function that ensures that a redirect target will lead to the same server."""

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc
