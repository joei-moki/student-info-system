import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.models.student import Student
from src.services.student_service import StudentService


class TestStudentService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        (self.root / "config").mkdir()
        (self.root / "data").mkdir()

        (self.root / "config" / "config.json").write_text(
            json.dumps({
                "data_file": "data/students.json",
                "log_file": "logs/test.log",
                "log_level": "INFO"
            }),
            encoding="utf-8"
        )

        (self.root / "data" / "students.json").write_text(
            "[]", encoding="utf-8"
        )

        self.path_patch = patch(
            "src.services.student_service.PROJECT_ROOT",
            self.root
        )
        self.path_patch.start()
        self.addCleanup(self.path_patch.stop)

        self.service = StudentService()

    def tearDown(self):
        self.temp_dir.cleanup()

    def make_student(self):
        return Student(
            student_id="S001",
            name="Alex Santos",
            age=20,
            course="BSIT",
            email="alex@example.com"
        )

    def test_add_and_reload_student(self):
        self.service.add_student(self.make_student())

        new_service = StudentService()
        self.assertEqual(len(new_service.get_all_students()), 1)
        self.assertEqual(new_service.get_student("S001").name,
                         "Alex Santos")

    def test_duplicate_student_id_is_rejected(self):
        self.service.add_student(self.make_student())

        with self.assertRaises(ValueError):
            self.service.add_student(self.make_student())

    def test_update_student(self):
        self.service.add_student(self.make_student())

        self.service.update_student(
            "S001", "Alex Cruz", 21, "BSIT", "alex@example.com"
        )

        self.assertEqual(
            self.service.get_student("S001").name, "Alex Cruz"
        )

    def test_delete_student(self):
        self.service.add_student(self.make_student())
        self.service.delete_student("S001")

        self.assertIsNone(self.service.get_student("S001"))
        self.assertEqual(self.service.get_all_students(), [])

    def test_missing_student_is_rejected(self):
        with self.assertRaises(ValueError):
            self.service.delete_student("UNKNOWN")


if __name__ == "__main__":
    unittest.main()