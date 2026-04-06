from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas import SetEntryCreate, SetEntryUpdate, SetEntry as SetEntrySchema
from models import ExerciseModel, SetEntryModel
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/exercises/{exercise_id}/sets", response_model=SetEntrySchema)
def create_set(
    exercise_id: int,
    set_entry: SetEntryCreate,
    db: Session = Depends(get_db)
):
    exercise = db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()

    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    db_set = SetEntryModel(
        exercise_id=exercise_id,
        set_number=set_entry.set_number,
        reps=set_entry.reps,
        weight=set_entry.weight
    )

    db.add(db_set)
    db.commit()
    db.refresh(db_set)

    return db_set


@router.get("/exercises/{exercise_id}/sets", response_model=list[SetEntrySchema])
def get_sets_for_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()

    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return db.query(SetEntryModel).filter(SetEntryModel.exercise_id == exercise_id).all()


@router.put("/sets/{set_id}", response_model=SetEntrySchema)
def update_set(
    set_id: int,
    updated_set: SetEntryUpdate,
    db: Session = Depends(get_db)
):
    set_entry = db.query(SetEntryModel).filter(SetEntryModel.id == set_id).first()

    if set_entry is None:
        raise HTTPException(status_code=404, detail="Set not found")

    update_data = updated_set.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(set_entry, key, value)

    db.commit()
    db.refresh(set_entry)

    return set_entry


@router.delete("/sets/{set_id}", response_model=SetEntrySchema)
def delete_set(set_id: int, db: Session = Depends(get_db)):
    set_entry = db.query(SetEntryModel).filter(SetEntryModel.id == set_id).first()

    if set_entry is None:
        raise HTTPException(status_code=404, detail="Set not found")

    db.delete(set_entry)
    db.commit()

    return set_entry