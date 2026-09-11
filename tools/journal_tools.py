from datetime import datetime, timezone

from sqlalchemy import select

from models.journal import JournalEntry
from models.conversation import Conversation, ChatMessage

from tools.database import SessionLocal


# ============================================================
# JOURNAL MEMORY
# ============================================================

def save_journal(
    content: str,
    analysis: dict,
    embedding: list[float],
) -> dict:

    with SessionLocal() as db:

        entry = JournalEntry(
            content=content,

            emotion=analysis.get(
                "emotion",
                "unknown"
            ),

            intensity=int(
                analysis.get(
                    "intensity",
                    0
                )
            ),

            topics=analysis.get(
                "topics",
                []
            ),

            event=analysis.get(
                "event",
                ""
            ),

            embedding=embedding
        )

        db.add(entry)

        db.commit()

        db.refresh(entry)

        return {
            "id": entry.id,
            "created_at": entry.created_at.isoformat()
        }


def search_memory(
    query_embedding: list[float],
    limit: int = 5,
) -> list[dict]:
    """
    Search ALL journal memories using pgvector.

    There is intentionally no 90-day limit.
    MindJournal should remember older experiences too.
    """

    with SessionLocal() as db:

        statement = (
            select(JournalEntry)
            .where(
                JournalEntry.embedding.is_not(None)
            )
            .order_by(
                JournalEntry.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
        )

        entries = db.scalars(
            statement
        ).all()

        return [
            {
                "id": entry.id,
                "content": entry.content,
                "emotion": entry.emotion,
                "intensity": entry.intensity,
                "topics": entry.topics,
                "event": entry.event,
                "created_at": entry.created_at.isoformat(),
            }
            for entry in entries
        ]


def recent_entries(
    limit: int = 10
) -> list[dict]:

    with SessionLocal() as db:

        statement = (
            select(JournalEntry)
            .order_by(
                JournalEntry.created_at.desc()
            )
            .limit(limit)
        )

        entries = db.scalars(
            statement
        ).all()

        return [
            {
                "id": entry.id,
                "content": entry.content,
                "emotion": entry.emotion,
                "intensity": entry.intensity,
                "topics": entry.topics,
                "event": entry.event,
                "created_at": entry.created_at.isoformat(),
            }
            for entry in entries
        ]


# ============================================================
# CONVERSATIONS
# ============================================================

def create_conversation(
    title: str = "MindJournal Conversation"
) -> int:

    with SessionLocal() as db:

        conversation = Conversation(
            title=title
        )

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        return conversation.id


def save_message(
    conversation_id: int,
    role: str,
    content: str,
) -> dict:

    with SessionLocal() as db:

        message = ChatMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)

        db.commit()

        db.refresh(message)

        return {
            "id": message.id,
            "conversation_id": message.conversation_id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
        }


def get_conversation_messages(
    conversation_id: int,
    limit: int = 20,
) -> list[dict]:

    with SessionLocal() as db:

        statement = (
            select(ChatMessage)
            .where(
                ChatMessage.conversation_id
                == conversation_id
            )
            .order_by(
                ChatMessage.created_at.desc()
            )
            .limit(limit)
        )

        messages = db.scalars(
            statement
        ).all()

        messages.reverse()

        return [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
            }
            for message in messages
        ]


def get_conversations(
    limit: int = 20,
) -> list[dict]:

    with SessionLocal() as db:

        statement = (
            select(Conversation)
            .order_by(
                Conversation.updated_at.desc()
            )
            .limit(limit)
        )

        conversations = db.scalars(
            statement
        ).all()

        return [
            {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
            }
            for conversation in conversations
        ]