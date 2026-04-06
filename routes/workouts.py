from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas import WorkoutCreate, WorkoutUpdate, Workout as WorkoutSchema
from models import WorkoutModel
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/workouts", response_model=list[WorkoutSchema])
def get_workouts(db: Session = Depends(get_db)):
    return db.query(WorkoutModel).all()


@router.get("/workouts/{workout_id}", response_model=WorkoutSchema)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(WorkoutModel).filter(WorkoutModel.id == workout_id).first()

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    return workout


@router.post("/workouts", response_model=WorkoutSchema)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = WorkoutModel(
        date=workout.date,
        workout_name=workout.workout_name,
        notes=workout.notes
    )

    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)

    return db_workout


@router.put("/workouts/{workout_id}", response_model=WorkoutSchema)
def update_workout(
    workout_id: int,
    updated_workout: WorkoutUpdate,
    db: Session = Depends(get_db)
):
    workout = db.query(WorkoutModel).filter(WorkoutModel.id == workout_id).first()

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    update_data = updated_workout.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(workout, key, value)

    db.commit()
    db.refresh(workout)

    return workout


@router.delete("/workouts/{workout_id}", response_model=WorkoutSchema)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(WorkoutModel).filter(WorkoutModel.id == workout_id).first()

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    db.delete(workout)
    db.commit()

    return workout