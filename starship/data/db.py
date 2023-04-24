from contextlib import AbstractContextManager, contextmanager
import sqlalchemy as sa
import os

import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

factory = None
engine = None

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


def global_init():
    global factory
    global engine

    if factory:
        return

    engine = sa.create_engine(get_db_url(), echo=False)
    engine.update_execution_options(connect_args={"connect_timeout": 5})
    factory = orm.sessionmaker(bind=engine, autocommit=False, autoflush=False)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def remove():
    global factory
    if factory:
        factory.close_all()


def make_thread_safe():
    if engine:
        engine.dispose()
    remove()


class session(AbstractContextManager):
    def __init__(self):
        global factory
        self.session = factory()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.session.rollback()
        self.session.close()
