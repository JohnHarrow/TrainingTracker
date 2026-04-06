#To Start:
#venv\Scripts\activate
#python -m uvicorn main:app --reload
#http://127.0.0.1:8000/docs

from fastapi import FastAPI
from database import engine
from models import Base
from routes import workouts, exercises, sets

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(sets.router)


@app.get("/")
def root():
    return {"message": "Workout Tracker API is running"}