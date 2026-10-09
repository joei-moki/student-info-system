import logging

from src.models.student import Student
from src.services.student_service import StudentService
from src.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


def display_students(students):
    """Display student records in a readable format."""
    if not students:
        print("\nNo student records found.")
        return

    print("\n" + "-" * 90)
    print(f"{'ID':<15}{'Name':<25}{'Age':<8}{'Course':<20}{'Email'}")
    print("-" * 90)

    for student in students:
        print(
            f"{student.student_id:<15}"
            f"{student.name:<25}"
            f"{student.age:<8}"
            f"{student.course:<20}"
            f"{student.email}"
        )

    print("-" * 90)


def read_student_details():
    """Ask for student information and validate it."""
    student_id = input("Student ID: ").strip()
    name = input("Full name: ").strip()
    age = int(input("Age: ").strip())
    course = input("Course: ").strip()
    email = input("Email: ").strip()

    return Student(
        student_id=student_id,
        name=name,
        age=age,
        course=course,
        email=email
    )


def main():
    """Run the interactive application."""
    try:
        setup_logging()
        service = StudentService()
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        print(f"Application startup failed: {error}")
        return

    print("\n=== Student Information System ===")

    while True:
        print(
            "\n1. Add Student"
            "\n2. View All Students"
            "\n3. Search Student"
            "\n4. Update Student"
            "\n5. Delete Student"
            "\n6. Exit"
        )

        choice = input("Choose an option (1-6): ").strip()

        try:
            if choice == "1":
                student = read_student_details()
                service.add_student(student)
                print("Student added successfully!")

            elif choice == "2":
                display_students(service.get_all_students())

            elif choice == "3":
                student_id = input("Enter student ID: ").strip()
                student = service.get_student(student_id)

                if student:
                    display_students([student])
                else:
                    print("Student not found.")

            elif choice == "4":
                student_id = input("Enter student ID to update: ").strip()

                if service.get_student(student_id) is None:
                    print("Student not found.")
                    continue

                name = input("New full name: ").strip()
                age = int(input("New age: ").strip())
                course = input("New course: ").strip()
                email = input("New email: ").strip()

                service.update_student(
                    student_id, name, age, course, email
                )
                print("Student updated successfully!")

            elif choice == "5":
                student_id = input("Enter student ID to delete: ").strip()
                service.delete_student(student_id)
                print("Student deleted successfully!")

            elif choice == "6":
                print("Thank you for using the Student Information System!")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 6.")

        except (ValueError, OSError, RuntimeError) as error:
            logger.warning("Operation failed: %s", error)
            print(f"Operation failed: {error}")

        except Exception:
            logger.exception("Unexpected application error.")
            print("An unexpected error occurred. Check logs/app.log.")


if __name__ == "__main__":
    main()