import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models.journal import Base, JournalEntry
from models.conversation import Conversation, ChatMessage


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is missing from .env"
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def init_db():
    """
    Initialize PostgreSQL database and create
    any missing MindJournal tables.
    """

    with engine.begin() as connection:

        connection.execute(
            text(
                "CREATE EXTENSION IF NOT EXISTS vector"
            )
        )

        Base.metadata.create_all(
            bind=connection
        )


def save_journal_entry(
    content: str,
    ai_analysis: str | None = None
):
    """
    Legacy helper used by the original Streamlit app.
    """

    db = SessionLocal()

    try:

        entry = JournalEntry(
            content=content,
            ai_analysis=ai_analysis,
        )

        db.add(entry)
        db.commit()
        db.refresh(entry)

        return entry

    finally:
        db.close()


def get_journal_entries(
    limit: int = 20
):
    db = SessionLocal()

    try:

        return (
            db.query(JournalEntry)
            .order_by(
                JournalEntry.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    finally:
        db.close()