from typing import Optional
from pydantic import BaseModel


class WorkoutCreate(BaseModel):
    date: str
    workout_name: str
    notes: str


class WorkoutUpdate(BaseModel):
    date: Optional[str] = None
    workout_name: Optional[str] = None
    notes: Optional[str] = None


class Workout(BaseModel):
    id: int
    date: str
    workout_name: str
    notes: str

    class Config:
        from_attributes = True


class ExerciseCreate(BaseModel):
    exercise_name: str


class ExerciseUpdate(BaseModel):
    exercise_name: Optional[str] = None


class Exercise(BaseModel):
    id: int
    workout_id: int
    exercise_name: str

    class Config:
        from_attributes = True


class SetEntryCreate(BaseModel):
    set_number: int
    reps: int
    weight: float


class SetEntryUpdate(BaseModel):
    set_number: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None


class SetEntry(BaseModel):
    id: int
    exercise_id: int
    set_number: int
    reps: int
    weight: float

    class Config:
        from_attributes = True