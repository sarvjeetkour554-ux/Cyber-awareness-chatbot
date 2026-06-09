import random
import streamlit as st

from utils.ollama_api import get_response
from utils.quiz_generator import get_random_quiz
from utils.pdf_export import create_pdf


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

h1 {
    text-align: center;
}

.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}

/* Chat Input Container */
[data-testid="stChatInput"] {
    background: #1e1e2f !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 30px !important;
    padding: 8px !important;
}

/* Remove all inner borders */
[data-testid="stChatInput"] > div {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* Text area */
[data-testid="stChatInput"] textarea {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* Focus state */
[data-testid="stChatInput"]:focus-within {
    border: 1px solid #3b82f6 !important;
    box-shadow: 0 0 10px rgba(59,130,246,0.4) !important;
}

/* Remove all red outlines */
textarea,
textarea:focus,
textarea:focus-visible,
input,
input:focus,
input:focus-visible {
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HEADER ----------------

st.markdown("""
#  🛡️Cyber Awareness Assistant
### Your Personal  CyberShield Chatbot
""")

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("⚙️ Settings")

    language = st.selectbox(
        "🌐 Select Language",
        ["English", "Hindi"]
    )

    st.divider()

    # Recent Questions

    st.subheader("💬 Recent Questions")

    user_messages = [
        msg["content"]
        for msg in st.session_state.messages
        if msg["role"] == "user"
    ]

    if len(user_messages) == 0:

        st.caption("No questions asked yet")

    else:

        for i, msg in enumerate(
            user_messages[-5:],
            start=1
        ):

            st.caption(
                f"{i}. {msg[:40]}"
            )

    st.divider()

    # Cyber Tips

    tips = [
        "Never share OTP with anyone.",
        "Enable Two-Factor Authentication.",
        "Use strong passwords.",
        "Keep software updated.",
        "Avoid suspicious links.",
        "Verify unknown emails before opening attachments."
    ]

    st.success(
        "💡 Cyber Tip\n\n" +
        random.choice(tips)
    )

    st.divider()

    # Cyber Quiz

    if st.button("🎯 Cyber Quiz"):

        quiz = get_random_quiz()

        st.info(
            f"Question:\n\n{quiz['question']}"
        )

        st.success(
            f"Answer:\n\n{quiz['answer']}"
        )

    st.divider()

    # Export PDF

    if st.button("📄 Export Chat PDF"):

        pdf_file = create_pdf(
            st.session_state.messages
        )

        st.success(
            f"Saved: {pdf_file}"
        )

    st.divider()

    # Clear Chat

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []
        st.rerun()

# ---------------- DASHBOARD ----------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Questions Asked",
        len(user_messages)
    )

with col2:

    st.metric(
        "Language",
        language
    )

with col3:

    st.metric(
        "Security Status",
        "Protected"
    )

# ---------------- WELCOME CARD ----------------

if len(st.session_state.messages) == 0:

    st.info("""
### 🔐 Ask About:

• Phishing Attacks
• Password Security
• UPI Frauds
• Email Scams
• Social Engineering
• Malware
• Ransomware
• Safe Browsing
• Cyber Awareness
""")

# ---------------- DISPLAY CHAT ----------------

for msg in st.session_state.messages:

    if msg["role"] == "user":

        with st.chat_message(
            "user",
            avatar="👨‍💻"
        ):
            st.write(
                msg["content"]
            )

    else:

        with st.chat_message(
            "assistant",
            avatar="🛡️"
        ):
            st.write(
                msg["content"]
            )

# ---------------- USER INPUT ----------------

user_input = st.chat_input(
    "🛡️ Ask anything about cybersecurity..."
)

# ---------------- PROCESS USER INPUT ----------------

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message(
        "user",
        avatar="👨‍💻"
    ):
        st.write(
            user_input
        )

    with st.spinner(
        "🛡️ Thinking..."
    ):

        answer = get_response(
            user_input,
            language
        )

    with st.chat_message(
        "assistant",
        avatar="🛡️"
    ):
        st.write(
            answer
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()