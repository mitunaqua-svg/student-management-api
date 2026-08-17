from pydantic import BaseModel, EmailStr, ConfigDict


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    course: str | None = None
    year: int | None = None


class StudentCreate(StudentBase):
    owner_id: int | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Jane Smith",
                "email": "jane@example.com",
                "course": "Computer Science",
                "year": 2,
                "owner_id": None,
            }
        }
    )


class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    course: str | None = None
    year: int | None = None


class StudentOut(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int | None = None