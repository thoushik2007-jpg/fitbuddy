def calculate_bmi(
    weight,
    height
):

    height_m = height / 100

    if height_m <= 0:

        return 0

    bmi = weight / (height_m * height_m)

    return round(bmi, 2)


def bmi_category(bmi):

    if bmi < 18.5:

        return "Underweight"

    elif bmi < 25:

        return "Normal range"

    elif bmi < 30:

        return "Overweight"

    else:

        return "Obesity range"


def get_basic_nutrition(
    weight,
    goal
):

    goal_lower = goal.lower()


    if "weight" in goal_lower:

        return """
NUTRITION FOCUS

• Include a protein source in each main meal.
• Eat plenty of vegetables.
• Choose fruits as convenient whole-food snacks.
• Prefer whole grains and minimally processed foods.
• Monitor portion sizes.
• Drink enough water.
• Avoid extreme calorie restriction.
• Maintain consistent sleep.
""".strip()


    if "muscle" in goal_lower:

        return """
NUTRITION FOCUS

• Include protein-rich foods throughout the day.
• Eat sufficient food to support training.
• Include carbohydrates around workouts.
• Eat vegetables and fruits regularly.
• Include healthy fats.
• Stay hydrated.
• Prioritize sleep and recovery.
""".strip()


    if "flexibility" in goal_lower:

        return """
NUTRITION FOCUS

• Eat balanced meals.
• Include adequate protein.
• Eat vegetables and fruits.
• Stay hydrated.
• Include whole-food carbohydrates.
• Maintain regular sleep.
• Support training with adequate recovery.
""".strip()


    return """
NUTRITION FOCUS

• Eat balanced meals.
• Include protein-rich foods.
• Eat vegetables and fruits.
• Choose whole grains regularly.
• Stay hydrated.
• Limit highly processed foods.
• Maintain consistent sleep and recovery.
""".strip()