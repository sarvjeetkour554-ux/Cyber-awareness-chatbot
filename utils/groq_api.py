from groq import Groq

import streamlit as st

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def get_response(user_input, language):

    if language == "Hindi":
        language_instruction = "Answer only in Hindi."
    else:
        language_instruction = "Answer only in English."

    prompt = f"""
You are a Cyber Awareness Assistant.

Rules:
- Answer only cybersecurity related questions.
- Explain in simple language.
- Give safety tips.
- Do not provide hacking instructions.

{language_instruction}

Question:
{user_input}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"