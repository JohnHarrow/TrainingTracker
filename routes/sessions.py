from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas import SessionCreate, SessionUpdate, Session as SessionSchema
from models import SessionModel
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/sessions", response_model=list[SessionSchema])
def get_sessions(db: Session = Depends(get_db)):
    return db.query(SessionModel).all()


@router.get("/sessions/{session_id}", response_model=SessionSchema)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.post("/sessions", response_model=SessionSchema)
def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    db_session = SessionModel(
        date=session.date,
        type=session.type,
        duration=session.duration,
        notes=session.notes
    )

    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return db_session


@router.put("/sessions/{session_id}", response_model=SessionSchema)
def update_session(
    session_id: int,
    updated_session: SessionUpdate,
    db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    update_data = updated_session.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(session, key, value)

    db.commit()
    db.refresh(session)

    return session


@router.delete("/sessions/{session_id}", response_model=SessionSchema)
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()

    return session