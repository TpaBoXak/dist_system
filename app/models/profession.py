from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
)


from .base import Base


class Profession(Base):
    __tablename__ = "professions"
    title: Mapped[str] = mapped_column(String(32), nullable=False)


class Experience(Base):
    __tablename__ = "experiences"
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False)
    prof_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("professions.id"), nullable=False)
    years: Mapped[int] = mapped_column(Integer, nullable=False)
