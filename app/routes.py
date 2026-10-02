from pathlib import Path

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db, User, WorkoutPlan
from app.schemas import FitnessInput
from app.gemini_generator import generate_workout_plan
from app.gemini_flash_generator import generate_nutrition_tip
from app.updated_plan import update_workout_plan
from app.nutrition import (
    calculate_bmi,
    bmi_category,
    get_basic_nutrition
)


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# =========================================================
# HOME PAGE
# =========================================================

@router.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# =========================================================
# GENERATE FITNESS PLAN
# =========================================================

@router.post("/generate")
def generate_plan(
    request: Request,

    name: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    height: float = Form(...),
    gender: str = Form(...),
    goal: str = Form(...),
    activity_level: str = Form(...),

    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Validate input
    # -----------------------------------------------------

    fitness_input = FitnessInput(
        name=name,
        user_id=user_id,
        age=age,
        weight=weight,
        height=height,
        gender=gender,
        goal=goal,
        activity_level=activity_level
    )


    # -----------------------------------------------------
    # Find existing user
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.user_id == fitness_input.user_id
        )
        .first()
    )


    # -----------------------------------------------------
    # Create new user
    # -----------------------------------------------------

    if user is None:

        user = User(
            user_id=fitness_input.user_id,
            name=fitness_input.name,
            age=fitness_input.age,
            weight=fitness_input.weight,
            height=fitness_input.height,
            gender=fitness_input.gender,
            goal=fitness_input.goal,
            activity_level=fitness_input.activity_level
        )

        db.add(user)


    # -----------------------------------------------------
    # Update existing user
    # -----------------------------------------------------

    else:

        user.name = fitness_input.name
        user.age = fitness_input.age
        user.weight = fitness_input.weight
        user.height = fitness_input.height
        user.gender = fitness_input.gender
        user.goal = fitness_input.goal
        user.activity_level = fitness_input.activity_level


    db.commit()
    db.refresh(user)


    # =====================================================
    # BMI CALCULATION
    # =====================================================

    bmi = calculate_bmi(
        fitness_input.weight,
        fitness_input.height
    )

    bmi_status = bmi_category(bmi)


    # =====================================================
    # AI WORKOUT PLAN
    # =====================================================

    workout_plan = generate_workout_plan(
        name=fitness_input.name,
        age=fitness_input.age,
        weight=fitness_input.weight,
        height=fitness_input.height,
        gender=fitness_input.gender,
        goal=fitness_input.goal,
        activity_level=fitness_input.activity_level
    )


    # =====================================================
    # AI NUTRITION TIP
    # =====================================================

    nutrition_tip = generate_nutrition_tip(
        name=fitness_input.name,
        age=fitness_input.age,
        weight=fitness_input.weight,
        height=fitness_input.height,
        gender=fitness_input.gender,
        goal=fitness_input.goal,
        activity_level=fitness_input.activity_level
    )


    # =====================================================
    # BASIC NUTRITION
    # =====================================================

    basic_nutrition = get_basic_nutrition(
        fitness_input.weight,
        fitness_input.goal
    )


    # =====================================================
    # SAVE WORKOUT PLAN
    # =====================================================

    plan = WorkoutPlan(
        user_id=user.id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    db.add(plan)

    db.commit()

    db.refresh(plan)


    # =====================================================
    # RESULT PAGE
    # =====================================================

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={

            "user_name": user.name,

            "user_age": user.age,

            "user_weight": user.weight,

            "user_height": user.height,

            "user_gender": user.gender,

            "user_goal": user.goal,

            "user_activity": user.activity_level,

            "bmi": bmi,

            "bmi_status": bmi_status,

            "workout_plan": workout_plan,

            "nutrition_tip": nutrition_tip,

            "basic_nutrition": basic_nutrition,

            "plan_id": plan.id,

            "plan": plan,

            "user": user
        }
    )


# =========================================================
# UPDATE PLAN USING FEEDBACK
# =========================================================

@router.post("/update-plan")
def update_plan(
    request: Request,

    plan_id: int = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Find workout plan
    # -----------------------------------------------------

    plan = (
        db.query(WorkoutPlan)
        .filter(
            WorkoutPlan.id == plan_id
        )
        .first()
    )


    if plan is None:

        return JSONResponse(
            status_code=404,
            content={
                "error": "Workout plan not found"
            }
        )


    # =====================================================
    # GENERATE UPDATED PLAN
    # =====================================================

    updated_plan = update_workout_plan(
        plan.original_plan,
        feedback
    )


    plan.updated_plan = updated_plan

    plan.feedback = feedback


    db.commit()

    db.refresh(plan)


    # =====================================================
    # GET USER
    # =====================================================

    user = (
        db.query(User)
        .filter(
            User.id == plan.user_id
        )
        .first()
    )


    # =====================================================
    # BMI
    # =====================================================

    bmi = calculate_bmi(
        user.weight,
        user.height
    )

    bmi_status = bmi_category(bmi)


    # =====================================================
    # BASIC NUTRITION
    # =====================================================

    basic_nutrition = get_basic_nutrition(
        user.weight,
        user.goal
    )


    # =====================================================
    # RESULT PAGE AFTER UPDATE
    # =====================================================

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={

            "user_name": user.name,

            "user_age": user.age,

            "user_weight": user.weight,

            "user_height": user.height,

            "user_gender": user.gender,

            "user_goal": user.goal,

            "user_activity": user.activity_level,

            "bmi": bmi,

            "bmi_status": bmi_status,

            "workout_plan": updated_plan,

            "nutrition_tip": plan.nutrition_tip,

            "basic_nutrition": basic_nutrition,

            "plan_id": plan.id,

            "plan": plan,

            "user": user
        }
    )


# =========================================================
# VIEW ALL USERS
# =========================================================

@router.get("/view-all-users")
def view_all_users(
    request: Request,

    db: Session = Depends(get_db)
):

    users = (
        db.query(User)
        .order_by(
            User.id.desc()
        )
        .all()
    )


    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users
        }
    )


# =========================================================
# API - ALL USERS
# =========================================================

@router.get("/api/users")
def api_users(
    db: Session = Depends(get_db)
):

    users = (
        db.query(User)
        .order_by(
            User.id.desc()
        )
        .all()
    )


    result = []


    for user in users:

        latest_plan = (
            db.query(WorkoutPlan)
            .filter(
                WorkoutPlan.user_id == user.id
            )
            .order_by(
                WorkoutPlan.id.desc()
            )
            .first()
        )


        result.append({

            "id": user.id,

            "user_id": user.user_id,

            "name": user.name,

            "age": user.age,

            "weight": user.weight,

            "height": user.height,

            "gender": user.gender,

            "goal": user.goal,

            "activity_level": user.activity_level,

            "latest_plan": (
                latest_plan.original_plan
                if latest_plan
                else None
            )
        })


    return {
        "users": result
    }