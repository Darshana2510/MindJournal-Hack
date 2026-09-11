from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector


EMBEDDING_DIMENSIONS = 768


class Base(DeclarativeBase):
    pass


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    ai_analysis: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    emotion: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="unknown"
    )

    intensity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    topics: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list
    )

    event: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=""
    )

    embedding: Mapped[list] = mapped_column(
        Vector(EMBEDDING_DIMENSIONS),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )