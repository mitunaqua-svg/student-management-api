from pydantic import BaseModel, EmailStr, ConfigDict


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    course: str | None = None
    year: int | None = None


class StudentCreate(StudentBase):
    owner_id: int | None = None


class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    course: str | None = None
    year: int | None = None


class StudentOut(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int | None = None