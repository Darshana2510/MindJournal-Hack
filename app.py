import streamlit as st
from datetime import datetime

from agent.journal_agent import JournalAgent
from tools.database import init_db
from tools.journal_tools import get_conversations


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MindJournal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DATABASE
# ============================================================

init_db()


# ============================================================
# AGENT
# ============================================================

@st.cache_resource
def load_agent():

    return JournalAgent()


agent = load_agent()


# ============================================================
# SESSION STATE
# ============================================================

if "conversation_id" not in st.session_state:

    st.session_state.conversation_id = (
        agent.start_conversation()
    )


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }


    /* Header */

    .mindjournal-header {
        text-align: center;
        padding: 12px 0 20px 0;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(90,70,160,0.08), rgba(120,190,180,0.05));
        margin-bottom: 16px;
    }

    .mindjournal-title {
        font-size: 2.7rem;
        font-weight: 800;
        margin-bottom: 6px;
        letter-spacing: -0.04em;
    }

    .mindjournal-subtitle {
        color: #777;
        font-size: 1rem;
    }


    /* Panel cards */

    .mindjournal-card {
        border: 1px solid rgba(180,180,180,0.16);
        border-radius: 18px;
        padding: 16px;
        background: rgba(255,255,255,0.045);
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        transition: transform 180ms ease, box-shadow 180ms ease;
    }

    .mindjournal-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.12);
    }

    .mindjournal-card-title {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #9a8bff;
        text-transform: uppercase;
    }

    .mindjournal-card-value {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 6px;
        color: #f8f8f8;
    }

    .mindjournal-card-note {
        font-size: 0.82rem;
        color: #bbbbbb;
    }


    /* Memory badge */

    .memory-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        background: rgba(100, 100, 100, 0.1);
        font-size: 0.8rem;
        margin-top: 8px;
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.2);
        background: rgba(18, 19, 26, 0.36);
    }


    /* Chat input */

    div[data-testid="stChatInput"] {
        padding-bottom: 20px;
    }

    div[data-testid="stChatInput"] textarea {
        border-radius: 16px;
        border: 1px solid rgba(160,160,160,0.2);
    }


    /* Streamlit widgets style */

    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 12px;
    }


    /* Hide Streamlit footer */

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🧠 MindJournal"
    )

    st.caption(
        "Your conversational journaling companion"
    )

    st.divider()

    # New conversation

    if st.button(
        "＋ New conversation",
        use_container_width=True,
        type="primary",
    ):

        st.session_state.conversation_id = (
            agent.start_conversation()
        )

        st.rerun()

    st.divider()

    # Quick reflection prompts

    st.markdown(
        "**Quick reflection prompts**"
    )

    quick_prompts = [
        "What felt heavy today?",
        "What made me feel proud?",
        "What am I avoiding?",
        "What helped me feel calm?",
    ]

    for prompt in quick_prompts:

        if st.button(
            prompt,
            key=f"prompt_{prompt}",
            use_container_width=True,
            type="secondary",
        ):

            st.session_state.quick_prompt = prompt
            st.rerun()

    st.divider()

    # Previous conversations

    st.markdown(
        "**Your conversations**"
    )

    conversations = get_conversations(
        limit=20
    )

    if conversations:

        for conversation in conversations:

            conversation_id = conversation["id"]

            label = (
                f"Conversation {conversation_id}"
            )

            is_current = (
                conversation_id
                == st.session_state.conversation_id
            )

            if st.button(
                label,
                key=f"conversation_{conversation_id}",
                use_container_width=True,
                type=(
                    "primary"
                    if is_current
                    else "secondary"
                ),
            ):

                st.session_state.conversation_id = (
                    conversation_id
                )

                st.rerun()

    else:

        st.caption(
            "Your conversations will appear here."
        )

    st.divider()

    # Helper status

    st.markdown(
        "**Today**"
    )

    st.caption(
        datetime.now().strftime("%A, %B %d, %Y")
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="mindjournal-header">

        <div class="mindjournal-title">
            🧠 MindJournal
        </div>

        <div class="mindjournal-subtitle">
            A private space to think, reflect, and be heard.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# UI CARDS
# ============================================================

plot_col1, plot_col2, plot_col3 = st.columns(3)

with plot_col1:

    st.markdown(
        """
        <div class="mindjournal-card">
            <div class="mindjournal-card-title">Reflection Flow</div>
            <div class="mindjournal-card-value">Calm</div>
            <div class="mindjournal-card-note">Start with one feeling</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with plot_col2:

    today_label = datetime.now().strftime("%b %d")

    st.markdown(
        f"""
        <div class="mindjournal-card">
            <div class="mindjournal-card-title">Today</div>
            <div class="mindjournal-card-value">{today_label}</div>
            <div class="mindjournal-card-note">Open reflection</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with plot_col3:

    conversation_count = len(get_conversations(limit=20))

    st.markdown(
        f"""
        <div class="mindjournal-card">
            <div class="mindjournal-card-title">Memory Thread</div>
            <div class="mindjournal-card-value">{conversation_count}</div>
            <div class="mindjournal-card-note">Conversations</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD CHAT HISTORY
# ============================================================

messages = agent.get_history(
    st.session_state.conversation_id,
    limit=100,
)


# ============================================================
# WELCOME MESSAGE
# ============================================================

if not messages:

    with st.chat_message(
        "assistant",
        avatar="🧠",
    ):

        st.markdown(
            """
            **Hi! I'm your MindJournal companion.**

            You can talk to me about whatever is on your mind —
            your day, your work, your relationships, your goals,
            frustrations, wins, or anything else.

            I'll remember meaningful things you share so that
            future conversations can have context.
            """
        )

        st.caption(
            "Nothing to organize. Just start talking."
        )


# ============================================================
# DISPLAY MESSAGES
# ============================================================

for message in messages:

    role = message["role"]

    avatar = (
        "🧠"
        if role == "assistant"
        else "👤"
    )

    with st.chat_message(
        role,
        avatar=avatar,
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

# Use a quick prompt from the sidebar if one was clicked.
user_message = st.session_state.get(
    "quick_prompt",
    None,
)

if user_message:
    # Claim the quick prompt in the visible chat workflow.
    st.session_state.quick_prompt = None

else:
    user_message = st.chat_input(
        "What's on your mind?"
    )


if user_message:

    # --------------------------------------------------------
    # Display user message immediately
    # --------------------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(
            user_message
        )


    # --------------------------------------------------------
    # Generate agent response
    # --------------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🧠",
    ):

        with st.spinner(
            "Thinking..."
        ):

            result = agent.chat(
                conversation_id=(
                    st.session_state.conversation_id
                ),
                user_message=user_message,
            )


        st.markdown(
            result["response"]
        )


        # ----------------------------------------------------
        # Memory indicator
        # ----------------------------------------------------

        memories = result.get(
            "memories",
            []
        )


        if memories:

            st.caption(
                f"🧠 I found "
                f"{len(memories)} relevant "
                f"memory"
                f"{'ies' if len(memories) != 1 else 'y'} "
                f"from your journal."
            )


    # --------------------------------------------------------
    # Rerun so message history is cleanly rendered
    # --------------------------------------------------------

    st.rerun()