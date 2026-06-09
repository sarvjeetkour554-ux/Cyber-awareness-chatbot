import requests

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

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]