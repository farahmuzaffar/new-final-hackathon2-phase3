from sqlmodel import create_engine, Session
from src.config import settings
from typing import Generator


# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session