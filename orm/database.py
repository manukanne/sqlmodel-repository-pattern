from typing import Callable

from sqlmodel import create_engine, Session

from settings import Settings


def create_sqlmodel_engine(settings: Settings, **kwargs):
    """Creates a SQLModel engine.

    Args:
        settings (Settings): Application settings.
        **kwargs: Engine parameters.

    Returns:
        Engine: SQLModel engine.
    """
    return create_engine(settings.database_connection_str, **kwargs)


def sqlmodel_session_maker(engine) -> Callable[[], Session]:
    """Returns a SQLModel session maker function.

    Args:
        engine (_type_): SQLModel engine.

    Returns:
        Callable[[], Session]: Session maker function.
    """
    return lambda: Session(bind=engine, autocommit=False, autoflush=False)
