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


class Project(Base):
    __tablename__ = "projects"
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    desc: Mapped[str] = mapped_column(String(256), nullable=False)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False)
    

class ProjectWorker(Base):
    __tablename__ = "projects_workers"
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=False)
    worker_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False)