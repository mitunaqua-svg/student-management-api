from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, students

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Auth",
        "description": "User registration, login (OAuth2 + JWT), and identity check.",
    },
    {
        "name": "Students",
        "description": "CRUD operations on student records, restricted by role (ADMIN / STUDENT).",
    },
]

app = FastAPI(
    title="Student Management API",
    description="A REST API for managing students with JWT authentication and role-based access control.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.include_router(auth.router)
app.include_router(students.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Student Management API is running.", "docs": "/docs"}