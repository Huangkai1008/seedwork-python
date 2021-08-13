import pytest

from sqlalchemy import Table, insert, select
from sqlalchemy.orm import sessionmaker

from seedwork.infrastructure.persistence.sqlalchemy import SQLAlchemyUnitOfWork


class TestSQLAlchemyUnitOfWork:
    def test_uow_can_retrieve_record_if_committed(
        self, session_factory: sessionmaker, table: Table
    ) -> None:
        uow = SQLAlchemyUnitOfWork(session_factory)
        with uow:
            stmt = insert(table).values(name='name', description='description')
            uow.session.execute(stmt)
            uow.session.commit()

        with uow:
            rows = uow.session.execute(select(table))
            assert len(list(rows)) == 1

    def test_uow_rollbacks_if_uncommitted(
        self, session_factory: sessionmaker, table: Table
    ) -> None:
        uow = SQLAlchemyUnitOfWork(session_factory)
        with uow:
            stmt = insert(table).values(name='name', description='description')
            uow.session.execute(stmt)

        with uow:
            rows = uow.session.execute(select(table))
            assert len(list(rows)) == 0

    def test_uow_rollbacks_on_error(
        self, session_factory: sessionmaker, table: Table
    ) -> None:

        uow = SQLAlchemyUnitOfWork(session_factory)
        with pytest.raises(Exception):
            with uow:
                stmt = insert(table).values(name='name', description='description')
                uow.session.execute(stmt)
                raise Exception()

        with uow:
            rows = uow.session.execute(select(table))
            assert len(list(rows)) == 0
