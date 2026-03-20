from fastapi import FastAPI

app = FastAPI()

sessions = []
session_id_counter = 1


@app.get("/")
def root():
    return {"message": "API is working"}


@app.post("/sessions")
def create_session(session: dict):
    global session_id_counter

    session["id"] = session_id_counter
    session_id_counter += 1

    sessions.append(session)
    return session