from __future__ import annotations

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# путь к файлу базы в корне проекта
BASE_DIR = Path(__file__).resolve().parents[2]  # .../psybook-main
DB_FILE = BASE_DIR / "psybook.sqlite3"
DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    from psybook.models.db_models import Base
    Base.metadata.create_all(bind=engine)
