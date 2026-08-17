from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, students

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API")

app.include_router(auth.router)
app.include_router(students.router)