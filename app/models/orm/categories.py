from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.postgres import Base

__all__ = ['Category']


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String)

    parent_id = Column(Integer, ForeignKey('categories.id'))
    code = Column(String, index=True, unique=True)

    created_at = Column(DateTime)

    def __repr__(self):
        return f"<Category(name={self.name})>"
