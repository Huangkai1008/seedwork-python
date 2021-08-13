from typing import Generator

import pytest
from sqlalchemy import Column, Engine, Integer, String, Table, create_engine
from sqlalchemy.orm import Session, registry, sessionmaker


@pytest.fixture(scope='session')
def engine(url: str = 'sqlite:///:memory:') -> Generator[Engine, None, None]:
    e = create_engine(url)

    yield e

    e.dispose()


@pytest.fixture
def table(engine: Engine) -> Generator[Table, None, None]:
    mapper_registry = registry()

    t = Table(
        'table',
        mapper_registry.metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('description', String),
    )

    mapper_registry.metadata.create_all(engine)

    yield t

    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def session_factory(
    engine: Engine, table: Table
) -> Generator[sessionmaker, None, None]:
    yield sessionmaker(bind=engine)


@pytest.fixture
def session(session_factory: sessionmaker) -> Session:
    return session_factory()  # type: ignore
