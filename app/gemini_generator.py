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


def demo_workout_plan(
    name,
    age,
    weight,
    height,
    gender,
    goal,
    activity_level
):

    return f"""
FITBUDDY - PERSONALIZED 7-DAY WORKOUT PLAN

Name: {name}
Age: {age}
Weight: {weight} kg
Height: {height} cm
Gender: {gender}
Goal: {goal}
Activity Level: {activity_level}


DAY 1 - FULL BODY

Warm-up:
• 5 minutes brisk walking
• Arm circles - 20 seconds
• Leg swings - 20 seconds

Main Workout:
• Bodyweight Squats - 3 sets × 12 reps
• Push-ups - 3 sets × 10 reps
• Glute Bridges - 3 sets × 15 reps
• Plank - 3 sets × 30 seconds

Cooldown:
• 5 minutes light stretching


DAY 2 - LOWER BODY

Warm-up:
• 5 minutes walking
• Leg swings
• Hip rotations

Main Workout:
• Squats - 3 × 12
• Reverse Lunges - 3 × 10 each leg
• Glute Bridges - 3 × 15
• Calf Raises - 3 × 15

Cooldown:
• Lower-body stretching


DAY 3 - ACTIVE RECOVERY

• 20-30 minutes comfortable walking
• Light stretching
• Mobility exercises


DAY 4 - UPPER BODY

Warm-up:
• Arm circles
• Shoulder rotations

Main Workout:
• Push-ups - 3 × 10
• Incline Push-ups - 3 × 12
• Backpack Rows - 3 × 12
• Shoulder Taps - 3 × 10 each side

Cooldown:
• Shoulder and chest stretching


DAY 5 - FULL BODY

Warm-up:
• 5 minutes walking
• Dynamic stretching

Main Workout:
• Squats - 3 × 12
• Push-ups - 3 × 10
• Lunges - 3 × 10 each leg
• Glute Bridges - 3 × 15
• Plank - 3 × 30 seconds

Cooldown:
• Full-body stretching


DAY 6 - LIGHT CARDIO

• 25-35 minutes walking
• Light mobility exercises
• Stretching


DAY 7 - REST AND RECOVERY

• Rest
• Optional easy walking
• Gentle stretching
• Proper hydration
• Good sleep


GENERAL GUIDELINES

• Start slowly.
• Maintain proper exercise technique.
• Stay hydrated.
• Rest when needed.
• Increase difficulty gradually.
• Stop exercising if you experience unusual pain or symptoms.
""".strip()


def generate_workout_plan(
    name,
    age,
    weight,
    height,
    gender,
    goal,
    activity_level
):

    if not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY":

        return demo_workout_plan(
            name,
            age,
            weight,
            height,
            gender,
            goal,
            activity_level
        )

    try:

        client = genai.Client(
            api_key=API_KEY
        )

        prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a personalized 7-day workout plan for this user.

USER INFORMATION

Name: {name}
Age: {age}
Weight: {weight} kg
Height: {height} cm
Gender: {gender}
Fitness Goal: {goal}
Activity Level: {activity_level}

REQUIREMENTS

1. Create exactly 7 days.
2. Include warm-up.
3. Include main exercises.
4. Include sets and repetitions or duration.
5. Include cooldown.
6. Include recovery/rest days where appropriate.
7. Match difficulty to the activity level.
8. Keep exercises practical.
9. Use simple language.
10. Do not diagnose medical conditions.
11. Do not provide medical treatment.
12. Do not recommend dangerous exercises.
13. Return plain text.
14. Do not return JSON.

Clearly label DAY 1 through DAY 7.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response.text:

            return response.text.strip()

    except Exception:

        pass

    return demo_workout_plan(
        name,
        age,
        weight,
        height,
        gender,
        goal,
        activity_level
    )