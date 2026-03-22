from fastapi import FastAPI

app = FastAPI()

sessions = []
session_id_counter = 1


@app.get("/")
def root():
    return {"message": "API is working"}


# Get all sessions
@app.get("/sessions")
def get_sessions():
    return sessions


# Get a single session by ID
@app.get("/sessions/{session_id}")
def get_session(session_id: int):
    for session in sessions:
        if session["id"] == session_id:
            return session
    return {"error": "Session not found"}


# Create a new session
@app.post("/sessions")
def create_session(session: dict):
    global session_id_counter

    session["id"] = session_id_counter
    session_id_counter += 1

    sessions.append(session)
    return session


# Update a session
@app.put("/sessions/{session_id}")
def update_session(session_id: int, updated_session: dict):
    for session in sessions:
        if session["id"] == session_id:
            updated_session.pop("id", None)  # prevent ID overwrite
            session.update(updated_session)
            return session
    return {"error": "Session not found"}


# Delete a session
@app.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    for i, session in enumerate(sessions):
        if session["id"] == session_id:
            return sessions.pop(i)
    return {"error": "Session not found"}