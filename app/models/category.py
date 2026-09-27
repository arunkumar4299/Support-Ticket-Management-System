from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base
class Category(Base):
    __tablename__ = "ticket_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
