from typing import Generator
from sqlalchemy.orm import Session
from app.core.postgres import SessionLocal


def get_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
