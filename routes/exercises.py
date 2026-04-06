from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas import ExerciseCreate, ExerciseUpdate, Exercise as ExerciseSchema
from models import WorkoutModel, ExerciseModel
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/workouts/{workout_id}/exercises", response_model=ExerciseSchema)
def create_exercise(
    workout_id: int,
    exercise: ExerciseCreate,
    db: Session = Depends(get_db)
):
    workout = db.query(WorkoutModel).filter(WorkoutModel.id == workout_id).first()

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    db_exercise = ExerciseModel(
        workout_id=workout_id,
        exercise_name=exercise.exercise_name
    )

    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)

    return db_exercise


@router.get("/workouts/{workout_id}/exercises", response_model=list[ExerciseSchema])
def get_exercises_for_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(WorkoutModel).filter(WorkoutModel.id == workout_id).first()

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    return db.query(ExerciseModel).filter(ExerciseModel.workout_id == workout_id).all()


@router.put("/exercises/{exercise_id}", response_model=ExerciseSchema)
def update_exercise(
    exercise_id: int,
    updated_exercise: ExerciseUpdate,
    db: Session = Depends(get_db)
):
    exercise = db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()

    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    update_data = updated_exercise.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(exercise, key, value)

    db.commit()
    db.refresh(exercise)

    return exercise


@router.delete("/exercises/{exercise_id}", response_model=ExerciseSchema)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()

    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    db.delete(exercise)
    db.commit()

    return exercise