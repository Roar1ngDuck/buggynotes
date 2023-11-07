# BuggyNotes - A Vulnerable Note Taking Web App

Welcome to the repository of BuggyNotes, the intentionally vulnerable web application made with Django. BuggyNotes is a simple, web-based note-taking application that has been deliberately crafted to include several security vulnerabilities from the OWASP Top 10 (2017). This project is part of a university course on cyber security.

## About BuggyNotes

BuggyNotes allows users to create an account, login, and save personal notes. However, due to its intentionally insecure nature, it contains the following vulnerabilities:

- **Broken Access Control**: The application does not properly verify that the user requesting a note is the note's owner, allowing any authenticated user to view any other users' notes.
- **Cross Site Scripting (XSS)**: User input is not properly validated or escaped, leading to persistent XSS where malicious scripts can be stored and executed.
- **Insecure Deserialization**: The application uses the `pickle` library for serializing and deserializing data, which is known to be vulnerable to arbitrary code execution if malicious data is deserialized.

## Installation
To set up the BuggyNotes, follow these steps:

_(Installation steps here...)_

## Usage
After installation, BuggyNotes will be accessible at `http://localhost:8000/` by default.

- **Register**: Create a new user account.
- **Login**: Log in with the user credentials.
- **Create Note**: Add new notes to your account.
- **View Note**: Edit your existing notes.
- **Backup Notes**: Create a backup of your notes.
- **Load Backup**: Restore notes from a backup file. (Note: This feature is vulnerable to insecure deserialization attacks.)

Please use this application in a safe and controlled environment. It is intended for educational purposes to understand and mitigate common web application vulnerabilities.
