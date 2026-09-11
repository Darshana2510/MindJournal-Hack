# MindJournal

## AI-Powered Personal Journal and Reflection Assistant

MindJournal is an AI-powered personal journaling assistant designed to help users not only record their thoughts and experiences, but also reflect on them and understand patterns over time.

---

## 1. Problem Statement

In today's fast-paced environment, people experience a large number of personal, academic, professional, and emotional events but often do not have enough time or a structured way to reflect on them.

Traditional journaling applications mainly provide a place to write and store journal entries. While this helps users record their experiences, the entries remain isolated. Users have to manually go through their previous journals to remember what they felt, what challenges they faced, and how their situation has changed over time.

This creates an important gap:

> **Journaling helps people record their experiences, but it does not necessarily help them understand the connections and patterns across those experiences.**

For example, a user may write several entries over a period of weeks about being stressed about a project. Later, they may feel more confident after completing it. A conventional journal stores both entries, but the user must manually connect these experiences.

MindJournal aims to solve this problem by making journaling more intelligent, contextual, and reflective.

---

## 2. Our Solution

MindJournal combines journaling with AI-based reflection and memory retrieval.

Instead of simply storing what the user writes, the system can:

1. Understand the current journal entry.
2. Identify important topics, emotions, or experiences.
3. Determine whether previous journal entries may provide useful context.
4. Retrieve relevant past entries.
5. Combine the current entry with relevant historical context.
6. Generate a personalized reflection for the user.

This allows the AI to help users see connections between their present thoughts and past experiences.

### Example

A user writes:

> "I finally feel confident about my project. I don't think I'm going to fail anymore."

MindJournal can retrieve an earlier relevant entry:

> "I'm worried that I won't be able to finish my project on time."

The system can then generate a reflection such as:

> "Your recent entries show a positive change in how you view the project. Earlier, you were concerned about completing it, while now you feel more confident. This suggests that your perception of the challenge has changed as you made progress."

The goal is not to tell users what they should feel, but to help them notice changes and patterns they may otherwise overlook.

---

## 3. Target Users

MindJournal is designed primarily for:

- Students
- Young adults
- Professionals
- Individuals who regularly journal
- People who want to reflect on their experiences
- Users interested in understanding their personal growth over time

---

## 4. Features

- 💬 Natural conversation with an AI agent
- 🗄️ Persistent memory — all chats stored in a database
- 🔁 Context retrieval from past sessions
- 🧭 Confidence/safety check on every response
- 🚨 Escalation flag for concerning entries

## 5. Tech Stack

Frontend / UI: Streamlit
Backend: Python
AI / LLM: Google Gemini
AI SDK: Google GenAI Python SDK
Embeddings: Gemini Embedding (gemini-embedding-001)
Database: PostgreSQL 17
Vector Database: pgvector
ORM: SQLAlchemy
Configuration: Python-dotenv (.env)
Memory: Semantic vector search + persistent conversation history
Version Control: Git & GitHub

Streamlit → Python Journal Agent → Gemini → Embeddings → PostgreSQL + pgvector → Semantic Memory Retrieval → Gemini Response

## 6. How MindJournal Works

The system follows an agentic workflow:
User
 ↓
Streamlit Chat Interface
 ↓
Safety & Crisis Detection
 ↓
Emotion + Intensity + Confidence Analysis
 ↓
Journal Entry Persistence
 ↓
Gemini Embedding Generation
 ↓
PostgreSQL + pgvector
 ↓
Semantic Memory Retrieval
 ↓
Conversation History + Relevant Past Memories
 ↓
Context Assembly
 ↓
Google Gemini Conversational Agent
 ↓
Personalized Emotional Reflection
 ↓
Save Conversation & Response
 ↓
Persistent Long-Term Memory


## 7. Setup

```
bash
git clone <repo-url>
cd mindjournal
pip install -r requirements.txt
cp .env.example .env   # add your Gemini API key + DB config
python app.py
```

## 8. Team
[NoviceX - Preethi Krishna, Darshana K, Nandana Sharan, Palak Joshi]



