from pydantic import BaseModel, Field


class FitnessInput(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    user_id: str = Field(
        min_length=2,
        max_length=50
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight: float = Field(
        gt=20,
        le=500
    )

    height: float = Field(
        gt=80,
        le=250
    )

    gender: str

    goal: str

    activity_level: str


class FeedbackInput(BaseModel):

    original_plan: str

    feedback: str = Field(
        min_length=3,
        max_length=3000
    )