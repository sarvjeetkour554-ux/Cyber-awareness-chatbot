import json
import random

def get_random_quiz():

    with open(
        "data/quiz.json",
        "r",
        encoding="utf-8"
    ) as f:

        questions = json.load(f)

    return random.choice(questions)