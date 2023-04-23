import sqlalchemy as sa
import os

import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy.orm.scoping import ScopedSession

SqlAlchemyBase = dec.declarative_base()

__factory = None
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
    global __factory
    global engine

    if __factory:
        return

    engine = sa.create_engine(get_db_url(), echo=False)
    engine.update_execution_options(connect_args={"connect_timeout": 5})
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def remove():
    global __factory
    if __factory:
        __factory.close_all()


def make_thread_safe():
    if engine:
        engine.dispose()
    remove()


def create_session() -> Session:
    global __factory
    return __factory()


def create_scoped_session() -> ScopedSession:
    global __factory
    return orm.scoped_session(__factory)()
