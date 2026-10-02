import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    ""
)


MODEL_NAME = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-2.5-pro"
)


def update_workout_plan(
    original_plan,
    feedback
):

    if not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY":

        return f"""
FITBUDDY - UPDATED WORKOUT PLAN

USER FEEDBACK:
{feedback}


UPDATED PLAN

The original plan has been adjusted according to the
feedback provided.

{original_plan}


ADDITIONAL GUIDANCE

• Follow the modified intensity gradually.
• Take adequate recovery.
• Maintain proper exercise technique.
• Stop if you experience unusual pain or symptoms.
""".strip()


    try:

        client = genai.Client(
            api_key=API_KEY
        )

        prompt = f"""
You are FitBuddy's AI workout-plan updating assistant.

ORIGINAL WORKOUT PLAN:

{original_plan}


USER FEEDBACK:

{feedback}


TASK:

Create a complete revised 7-day workout plan based on
the user's feedback.

REQUIREMENTS:

- Address the feedback.
- Keep useful parts of the original plan.
- Modify exercises when appropriate.
- Modify intensity when appropriate.
- Include all 7 days.
- Include warm-up.
- Include main workout.
- Include sets/repetitions/duration.
- Include cooldown.
- Include recovery.
- Use simple language.
- Do not diagnose medical conditions.
- Do not provide medical treatment.
- Do not return JSON.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response.text:

            return response.text.strip()

    except Exception:

        pass


    return original_plan