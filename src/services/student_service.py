import json
import logging
from pathlib import Path

from src.models.student import Student

logger = logging.getLogger(__name__)

# Find the project root independently of the terminal's location.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"


class StudentService:
    """Handles student records and persistent JSON storage."""

    def __init__(self):
        try:
            with CONFIG_PATH.open("r", encoding="utf-8") as file:
                config = json.load(file)

            self.data_file = PROJECT_ROOT / config["data_file"]
            self.data_file.parent.mkdir(parents=True, exist_ok=True)

            if not self.data_file.exists():
                self.data_file.write_text("[]", encoding="utf-8")

            self.students = self._load_students()
            logger.info("Student service initialized.")

        except (OSError, json.JSONDecodeError, KeyError) as error:
            logger.exception("Could not initialize student service.")
            raise RuntimeError(
                f"Could not initialize the application: {error}"
            ) from error

    def _load_students(self):
        """Load and validate saved records."""
        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                records = json.load(file)

            if not isinstance(records, list):
                raise ValueError("Student JSON data must be a list.")

            students = [Student.from_dict(item) for item in records]

            ids = [student.student_id for student in students]
            if len(ids) != len(set(ids)):
                raise ValueError("Duplicate student IDs found in JSON.")

            logger.info("Loaded %d student records.", len(students))
            return students

        except (OSError, json.JSONDecodeError, KeyError, TypeError,
                ValueError) as error:
            logger.exception("Failed to load student records.")
            raise RuntimeError(
                f"Could not load student records: {error}"
            ) from error

    def _save_students(self):
        """Persist all current records to JSON."""
        try:
            with self.data_file.open("w", encoding="utf-8") as file:
                json.dump(
                    [student.to_dict() for student in self.students],
                    file,
                    indent=4
                )

            logger.info("Student records saved successfully.")

        except (OSError, TypeError, ValueError):
            logger.exception("Failed to save student records.")
            raise

    def add_student(self, student):
        """Add a student with a unique ID."""
        if any(s.student_id == student.student_id
               for s in self.students):
            raise ValueError("That student ID already exists.")

        self.students.append(student)

        try:
            self._save_students()
        except OSError:
            self.students.pop()
            raise

        logger.info("Added student ID %s.", student.student_id)

    def get_all_students(self):
        """Return all student records."""
        return list(self.students)

    def get_student(self, student_id):
        """Find one student by ID."""
        student_id = str(student_id).strip()

        for student in self.students:
            if student.student_id == student_id:
                return student

        return None

    def update_student(self, student_id, name, age, course, email):
        """Update an existing student's information."""
        student = self.get_student(student_id)

        if student is None:
            raise ValueError("Student not found.")

        # Validate the new information before changing the record.
        updated = Student(
            student_id=student.student_id,
            name=name,
            age=age,
            course=course,
            email=email
        )

        old_values = student.to_dict()
        student.name = updated.name
        student.age = updated.age
        student.course = updated.course
        student.email = updated.email

        try:
            self._save_students()
        except OSError:
            student.name = old_values["name"]
            student.age = old_values["age"]
            student.course = old_values["course"]
            student.email = old_values["email"]
            raise

        logger.info("Updated student ID %s.", student.student_id)

    def delete_student(self, student_id):
        """Delete a student record by ID."""
        student = self.get_student(student_id)

        if student is None:
            raise ValueError("Student not found.")

        self.students.remove(student)

        try:
            self._save_students()
        except OSError:
            self.students.append(student)
            raise

        logger.info("Deleted student ID %s.", student.student_id)