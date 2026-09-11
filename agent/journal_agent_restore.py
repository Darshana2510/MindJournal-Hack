import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts.prompts import (
    ANALYZE_PROMPT,
    CONVERSATION_PROMPT,
)

from tools.database import init_db

from tools.journal_tools import (
    create_conversation,
    get_conversation_messages,
    save_message,
    save_journal,
    search_memory,
)


load_dotenv()


GENERATION_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)

EMBEDDING_MODEL = os.getenv(
    "GEMINI_EMBEDDING_MODEL",
    "gemini-embedding-001"
)


class JournalAgent:

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing from .env"
            )

        self.client = genai.Client(
            api_key=api_key
        )

        init_db()


    # ========================================================
    # GEMINI
    # ========================================================

    def _embed(
        self,
        text: str
    ) -> list[float]:

        result = self.client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=768
            ),
        )

        return list(
            result.embeddings[0].values
        )


    def _generate(
        self,
        prompt: str,
        max_output_tokens: int = 700,
    ) -> str:

        response = self.client.models.generate_content(
            model=GENERATION_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=max_output_tokens,
            ),
        )

        return (
            response.text.strip()
            if response.text
            else ""
        )


    # ========================================================
    # ANALYZE MEMORY
    # ========================================================

    def analyze_entry(
        self,
        entry: str
    ) -> dict:

        raw = self._generate(
            ANALYZE_PROMPT.format(
                entry=entry
            ),
            max_output_tokens=300,
        )

        cleaned = raw.strip()

        if cleaned.startswith("```"):

            cleaned = (
                cleaned
                .replace("```json", "", 1)
                .replace("```", "", 1)
                .strip()
            )

        try:

            data = json.loads(
                cleaned
            )

        except json.JSONDecodeError:

            data = {
                "emotion": "unknown",
                "intensity": 1,
                "topics": [],
                "event": "",
            }

        try:

            data["intensity"] = max(
                1,
                min(
                    10,
                    int(
                        data.get(
                            "intensity",
                            1
                        )
                    )
                )
            )

        except (
            TypeError,
            ValueError
        ):

            data["intensity"] = 1

        data["emotion"] = str(
            data.get(
                "emotion",
                "unknown"
            )
        )

        data["topics"] = (
            data.get(
                "topics",
                []
            )
            or []
        )

        data["event"] = str(
            data.get(
                "event",
                ""
            )
        )

        return data


    # ========================================================
    # CONVERSATION
    # ========================================================

    def start_conversation(self) -> int:

        return create_conversation()


    def get_history(
        self,
        conversation_id: int,
        limit: int = 20,
    ) -> list[dict]:

        return get_conversation_messages(
            conversation_id,
            limit=limit
        )


    def chat(
        self,
        conversation_id: int,
        user_message: str,
    ) -> dict:

        user_message = user_message.strip()

        if not user_message:

            return {
                "response": (
                    "I'm here. Tell me what's on your mind."
                ),
                "memories": [],
                "analysis": {},
            }


        # ----------------------------------------------------
        # STEP 1
        # Analyze what the user is feeling
        # ----------------------------------------------------

        analysis = self.analyze_entry(
            user_message
        )


        # ----------------------------------------------------
        # STEP 2
        # Create semantic embedding
        # ----------------------------------------------------

        embedding = self._embed(
            user_message
        )


        # ----------------------------------------------------
        # STEP 3
        # Save the user's message as long-term memory
        # ----------------------------------------------------

        saved_memory = save_journal(
            content=user_message,
            analysis=analysis,
            embedding=embedding,
        )


        # ----------------------------------------------------
        # STEP 4
        # Save message to current conversation
        # ----------------------------------------------------

        save_message(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
        )


        # ----------------------------------------------------
        # STEP 5
        # Search long-term memories
        # ----------------------------------------------------

        memories = search_memory(
            query_embedding=embedding,
            limit=5,
        )


        # Don't retrieve the exact message we just saved

        memories = [
            memory
            for memory in memories
            if memory["id"]
            != saved_memory["id"]
        ]


        # ----------------------------------------------------
        # STEP 6
        # Load current conversation history
        # ----------------------------------------------------

        history = get_conversation_messages(
            conversation_id,
            limit=20,
        )


        conversation_text = "\n".join(
            (
                f"{message['role'].upper()}: "
                f"{message['content']}"
            )
            for message in history
        )


        if not conversation_text:

            conversation_text = (
                "No previous conversation."
            )


        # ----------------------------------------------------
        # STEP 7
        # Format long-term memories
        # ----------------------------------------------------

        if memories:

            memory_text = "\n\n".join(
                (
                    f"Memory {index + 1}:\n"
                    f"Date: {memory['created_at']}\n"
                    f"Emotion: {memory['emotion']}\n"
                    f"Intensity: {memory['intensity']}\n"
                    f"Topics: {memory['topics']}\n"
                    f"Event: {memory['event']}\n"
                    f"Content: {memory['content']}"
                )
                for index, memory
                in enumerate(memories)
            )

        else:

            memory_text = (
                "No relevant long-term memories found."
            )


        # ----------------------------------------------------
        # STEP 8
        # Ask Gemini to respond
        # ----------------------------------------------------

        prompt = CONVERSATION_PROMPT.format(
            conversation=conversation_text,
            memories=memory_text,
            current_message=user_message,
        )


        response = self._generate(
            prompt,
            max_output_tokens=700,
        )


        if not response:

            response = (
                "I'm here with you. "
                "Would you like to tell me more?"
            )


        # ----------------------------------------------------
        # STEP 9
        # Save AI response
        # ----------------------------------------------------

        save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=response,
        )


        # ----------------------------------------------------
        # STEP 10
        # Return everything the UI needs
        # ----------------------------------------------------

        return {
            "response": response,
            "memories": memories,
            "analysis": analysis,
        }
