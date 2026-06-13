

import random
import streamlit as st

from utils.groq_api import get_response
from utils.quiz_generator import get_random_quiz
from utils.pdf_export import create_pdf


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Cyber Awareness Assistant",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Title */
h1 {
    text-align: center;
}

/* Chat messages */
.stChatMessage {
    border-radius: 15px;
    padding: 5px;
}

/* Chat Input Container */
[data-testid="stChatInput"] {
    border: 1px solid #3b82f6 !important;
    border-radius: 30px !important;
    padding: 8px !important;
}

/* Remove inner borders */
[data-testid="stChatInput"] > div {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* Auto theme support */
[data-testid="stChatInput"] textarea {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: inherit !important;
    color: inherit !important;
}

/* Focus effect */
[data-testid="stChatInput"]:focus-within {
    border: 1px solid #3b82f6 !important;
    box-shadow: 0 0 8px rgba(59,130,246,0.3) !important;
}

/* Remove red outlines */
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

/* Mobile Optimization */
@media (max-width: 768px) {

    h1 {
        font-size: 26px !important;
    }

    .stMarkdown {
        font-size: 14px !important;
    }

    [data-testid="stMetric"] {
        text-align: center !important;
    }

    [data-testid="stChatInput"] {
        border-radius: 20px !important;
        padding: 6px !important;
    }
}

</style>
""", unsafe_allow_html=True)



# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HEADER ----------------

st.markdown("""
#  🛡️Cyber Awareness Assistant
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

# ---------------- DASHBOARD ----------------

st.markdown(f"""
<div style="
display:flex;
justify-content:space-around;
align-items:center;
text-align:center;
margin-bottom:20px;
">

<div>
<p style="margin:0;font-size:12px;">Questions</p>
<h3>{len(user_messages)}</h3>
</div>

<div>
<p style="margin:0;font-size:12px;">Language</p>
<h3>{language}</h3>
</div>

<div>
<p style="margin:0;font-size:12px;">Status</p>
<h3>Protected</h3>
</div>

</div>
""", unsafe_allow_html=True)


# ---------------- WELCOME CARD ----------------

if len(st.session_state.messages) == 0:

   st.caption(
    "🔐 Phishing • Passwords • UPI Frauds • Email Scams • Malware • Ransomware"
)

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