from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    course = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)

    owner = relationship("User", backref="student_profile")