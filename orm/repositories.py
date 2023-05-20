from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Optional, List

from sqlmodel import Session, select, and_
from sqlmodel.sql.expression import SelectOfScalar

from schemas import BaseModel, Hero, Team

T = TypeVar("T", bound=BaseModel)


class GenericRepository(Generic[T], ABC):
    """Generic base repository.
    """

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Get a single record by id.

        Args:
            id (int): Record id.

        Returns:
            Optional[T]: Record or none.
        """
        raise NotImplementedError()

    @abstractmethod
    def list(self, **filters) -> List[T]:
        """Gets a list of records

        Args:
            **filters: Filter conditions, several criteria are linked with a logical 'and'.

         Raises:
            ValueError: Invalid filter condition.

        Returns:
            List[T]: List of records.
        """
        raise NotImplementedError()

    @abstractmethod
    def add(self, record: T) -> T:
        """Creates a new record.

        Args:
            record (T): The record to be created.

        Returns:
            T: The created record.
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, record: T) -> T:
        """Updates an existing record.

        Args:
            record (T): The record to be updated incl. record id.

        Returns:
            T: The updated record.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: int) -> None:
        """Deletes a record by id.

        Args:
            id (int): Record id.
        """
        raise NotImplementedError()


class GenericSqlRepository(GenericRepository[T], ABC):
    """Generic SQL Repository.
    """
    def __init__(self, session: Session, model_cls: Type[T]) -> None:
        """Creates a new repository instance.

        Args:
            session (Session): SQLModel session.
            model_cls (Type[T]): SQLModel class type.
        """
        self._session = session
        self._model_cls = model_cls

    def _construct_get_stmt(self, id: int) -> SelectOfScalar:
        """Creates a SELECT query for retrieving a single record.

        Args:
            id (int):  Record id.

        Returns:
            SelectOfScalar: SELECT statement.
        """
        stmt = select(self._model_cls).where(self._model_cls.id == id)
        return stmt

    def get_by_id(self, id: int) -> Optional[T]:
        stmt = self._construct_get_stmt(id)
        return self._session.exec(stmt).first()

    def _construct_list_stmt(self, **filters) -> SelectOfScalar:
        """Creates a SELECT query for retrieving a multiple records.

        Raises:
            ValueError: Invalid column name.

        Returns:
            SelectOfScalar: SELECT statment.
        """
        stmt = select(self._model_cls)
        where_clauses = []
        for c, v in filters.items():
            if not hasattr(self._model_cls, c):
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self._model_cls, c) == v)

        if len(where_clauses) == 1:
            stmt = stmt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmt.where(and_(*where_clauses))
        return stmt

    def list(self, **filters) -> List[T]:
        stmt = self._construct_list_stmt(**filters)
        return self._session.exec(stmt).all()

    def add(self, record: T) -> T:
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    def update(self, record: T) -> T:
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    def delete(self, id: int) -> None:
        record = self.get_by_id(id)
        if record is not None:
            self._session.delete(record)


class HeroReposityBase(GenericRepository[Hero], ABC):
    """Hero repository.
    """
    ...


class HeroRepository(GenericSqlRepository[Hero], HeroReposityBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Hero)


class TeamRepositoryBase(GenericRepository[Team], ABC):
    """Team repository.
    """


class TeamRepository(GenericSqlRepository[Team], TeamRepositoryBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Team)
