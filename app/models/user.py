from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from sqlalchemy import (
    DateTime, 
    Date,
    String,
    Integer,
    ForeignKey,
    func
)

from datetime import (
    datetime,
    date
)

from .base import Base

class User(Base):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    second_name: Mapped[str] = mapped_column(String(32), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(32), nullable=False)
    birthday: Mapped[date] = mapped_column(Date)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_roles.id"))
    time_created: Mapped[datetime] = mapped_column(DateTime, nullable=False,
            server_default=func.now())
    
class UserRole(Base):
    __tablename__ = "users_roles"
    title: Mapped[str] = mapped_column(String(32), nullable=False)