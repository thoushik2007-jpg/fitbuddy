import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    ""
)


MODEL_NAME = os.getenv(
    "GEMINI_FAST_MODEL",
    "gemini-2.5-flash"
)


def generate_nutrition_tip(
    name,
    age,
    weight,
    height,
    gender,
    goal,
    activity_level
):

    default_tip = """
Focus on balanced meals containing adequate protein,
vegetables, fruits, whole-food carbohydrates and healthy fats.
Stay hydrated and prioritize sufficient sleep and recovery.
Avoid extreme dieting and make gradual sustainable changes.
""".strip()


    if not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY":

        return default_tip


    try:

        client = genai.Client(
            api_key=API_KEY
        )

        prompt = f"""
You are FitBuddy's AI nutrition assistant.

User information:

Name: {name}
Age: {age}
Weight: {weight} kg
Height: {height} cm
Gender: {gender}
Goal: {goal}
Activity Level: {activity_level}

Give practical nutrition and recovery advice.

Requirements:
- 3 to 5 sentences.
- Simple language.
- Balanced food recommendations.
- Mention protein when appropriate.
- Mention hydration.
- Mention sleep/recovery.
- No extreme dieting.
- No medical diagnosis.
- No medical treatment.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response.text:

            return response.text.strip()

    except Exception:

        pass


    return default_tip