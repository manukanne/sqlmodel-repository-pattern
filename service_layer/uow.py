from abc import ABC, abstractmethod
from typing import Callable

from orm.repositories import (
    HeroReposityBase,
    TeamRepositoryBase,
    HeroRepository,
    TeamRepository
)

from sqlmodel import Session


class UnitOfWorkBase(ABC):
    """Unit of work.
    """

    heroes: HeroReposityBase
    teams: TeamRepositoryBase

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.rollback()

    @abstractmethod
    def commit(self):
        """Commits the current transaction.
        """
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        """Rollbacks the current transaction.
        """
        raise NotImplementedError()


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        """Creates a new uow instance.

        Args:
            session_factory (Callable[[], Session]): Session maker function.
        """
        self._session_factory = session_factory

    def __enter__(self):
        self._session = self._session_factory()
        self.heroes = HeroRepository(self._session)
        self.teams = TeamRepository(self._session)
        return super().__enter__()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
