
# Student Information System

## Project Overview

The Student Information System is a Python application that manages
student information using JSON file storage.

It demonstrates modular programming, configuration management,
error handling, logging, and Git version control.

## Features

- Add new student records
- View all student records
- Search students by ID
- Update student information
- Delete student records
- Save records in JSON format
- Log application activities and errors

## Technologies Used

- Python 3
- JSON
- Git and GitHub
- VS Code

## Project Structure

```text
student-info-system/
├── config/
│   └── config.json
├── data/
│   └── students.json
├── logs/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── student.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── student_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logging_config.py
│   └── main.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10 or newer
- Visual Studio Code (recommended)
- Git (for version control)

## How to Run

1. Open the project folder in VS Code.
2. Open the terminal in the project root.
3. Run the application:

   `python -m src.main`

## Data Storage

Student records are stored in `data/students.json`.
Application logs are stored in `logs/app.log`.

## Limitations

- The current version is a command-line application.
- JSON storage is suitable for a small demonstration, not concurrent
  multi-user production use.
- Authentication and role-based access control are not implemented.
- XML storage is not implemented in this version.

## Future Improvements

- Add a graphical or web interface.
- Add user authentication and access control.
- Support XML storage.
- Use a database for concurrent users.
- Deploy the application to a cloud environment.

## Author

Student Information System Project