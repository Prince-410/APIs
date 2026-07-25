import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Environment variable for database URL
# MySQL default URL format: mysql+pymysql://<user>:<password>@<host>:<port>/<dbname>
# Default fallback to SQLite if DATABASE_URL is not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./notes.db")

# Engine options based on database dialect
engine_kwargs = {
    "echo": False,  # Set to True to log raw SQL queries
}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # MySQL / PostgreSQL connection pooling optimization
    engine_kwargs["pool_pre_ping"] = True  # Automatically re-establish broken connections
    engine_kwargs["pool_recycle"] = 3600   # Recycle connections after 1 hour

engine = create_engine(
    DATABASE_URL,
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that creates a new database session per request
    and closes it when the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
