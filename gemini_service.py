import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Add it to your .env file."
    )

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.7,
    max_output_tokens: int = 1000,
) -> str:
    """
    Generate a response using Google Gemini.
    """

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config,
    )

    if not response.text:
        return "I wasn't able to generate a response."

    return response.text.strip()


def analyze_journal_entry(journal_text: str) -> str:
    """
    Analyze a journal entry and provide a supportive reflection.
    """

    system_instruction = """
You are MindJournal, a compassionate AI journaling assistant.

Your role is to help users reflect on their journal entries.

Analyze the user's writing carefully and identify:
- emotional themes
- possible sources of stress
- positive experiences
- recurring thoughts
- patterns worth reflecting on
- gentle suggestions for self-reflection

Be supportive, non-judgmental, and concise.

Do not diagnose mental health conditions.
Do not claim to be a therapist or doctor.
Do not make medical diagnoses.

If the user appears to be in immediate danger or expresses
intent to harm themselves or someone else, encourage them to
seek immediate help from a trusted person or appropriate
emergency/crisis service.

Return a clear, human-friendly response.
"""

    prompt = f"""
Here is the user's journal entry:

--- JOURNAL ENTRY ---
{journal_text}
--- END JOURNAL ENTRY ---

Please provide:

1. Emotional summary
2. Key themes
3. Positive observations
4. Things worth reflecting on
5. One gentle reflection question

Keep the response supportive and easy to read.
"""

    return generate_response(
        prompt=prompt,
        system_instruction=system_instruction,
        temperature=0.6,
        max_output_tokens=800,
    )


def generate_journal_prompt() -> str:
    """
    Generate a journaling prompt.
    """

    system_instruction = """
You are a thoughtful journaling assistant.
Generate a single meaningful journaling prompt.

The prompt should encourage self-reflection without being
judgmental or overly clinical.
"""

    return generate_response(
        prompt="Give me one thoughtful journal prompt for today.",
        system_instruction=system_instruction,
        temperature=0.8,
        max_output_tokens=150,
    )


def generate_daily_insight(journal_text: str) -> str:
    """
    Generate a short daily insight from a journal entry.
    """

    system_instruction = """
You are MindJournal.

Give the user a short, encouraging insight based on their
journal entry.

Do not diagnose.
Do not make medical claims.
Focus on reflection, emotions, habits, gratitude,
relationships, goals, and personal growth.
"""

    prompt = f"""
Journal entry:

{journal_text}

Give me one short personal insight I can reflect on today.
"""

    return generate_response(
        prompt=prompt,
        system_instruction=system_instruction,
        temperature=0.7,
        max_output_tokens=250,
    )