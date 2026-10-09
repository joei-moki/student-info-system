
"""Defines the Student data model."""

from dataclasses import dataclass, asdict


@dataclass
class Student:
    student_id: str
    name: str
    age: int
    course: str
    email: str

    def __post_init__(self):
        self.student_id = str(self.student_id).strip()
        self.name = self.name.strip()
        self.course = self.course.strip()
        self.email = self.email.strip()

        if not self.student_id:
            raise ValueError("Student ID cannot be empty.")

        if not self.name:
            raise ValueError("Student name cannot be empty.")

        if not isinstance(self.age, int) or isinstance(self.age, bool):
            raise ValueError("Age must be a whole number.")

        if not 1 <= self.age <= 120:
            raise ValueError("Age must be between 1 and 120.")

        if not self.course:
            raise ValueError("Course cannot be empty.")

        if "@" not in self.email or "." not in self.email.split("@")[-1]:
            raise ValueError("Please enter a valid email address.")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            course=data["course"],
            email=data["email"]
        )