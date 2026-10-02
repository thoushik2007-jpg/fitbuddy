from pathlib import Path
from datetime import datetime, timezone

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
)
from dotenv import load_dotenv
import os


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'fitbuddy.db'}"
)


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    weight = Column(
        Float,
        nullable=False
    )

    height = Column(
        Float,
        nullable=False
    )

    gender = Column(
        String(20),
        nullable=False
    )

    goal = Column(
        String(100),
        nullable=False
    )

    activity_level = Column(
        String(50),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    plans = relationship(
        "WorkoutPlan",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class WorkoutPlan(Base):

    __tablename__ = "workout_plans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    original_plan = Column(
        Text,
        nullable=False
    )

    updated_plan = Column(
        Text,
        nullable=True
    )

    nutrition_tip = Column(
        Text,
        nullable=True
    )

    feedback = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    user = relationship(
        "User",
        back_populates="plans"
    )


def init_db():

    Base.metadata.create_all(
        bind=engine
    )


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()