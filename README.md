# BuggyNotes - A Vulnerable Note Taking Web App

Welcome to the repository of BuggyNotes, the intentionally vulnerable web application made with Django. BuggyNotes is a simple, web-based note-taking application that has been deliberately crafted to include several security vulnerabilities from the OWASP Top 10 (2017). This project is part of a university course on cyber security.

## About BuggyNotes

BuggyNotes allows users to create an account, login, and save personal notes. However, due to its intentionally insecure nature, it contains the following vulnerabilities:

- **SQL Injection**: The note searching function places user inputted text directly in the SQL query, without sanitizng it or using a parametrized query, resulting in an SQL injection vulnerability.
- **Broken Access Control**: The application does not properly verify that the user requesting a note is the note's owner, allowing any authenticated user to view any other users' notes.
- **Cross Site Scripting (XSS)**: User input is not properly validated or escaped, leading to persistent XSS in the note content where malicious scripts can be stored and executed.
- **Insecure Deserialization**: The application uses the `pickle` library for serializing and deserializing note backups, which is known to be vulnerable to arbitrary code execution if malicious data is deserialized.
- **XML External Entities (XXE)**: Unnecessary whitespace and comments are removed from user drawn SVG images before saving, however by using `etree.XMLParser` with default settings to parse them, the application is exposed to an XXE vulnerability.

## Installation
To set up the BuggyNotes, follow these steps:

1. Clone the repository: ```git clone https://github.com/Roar1ngDuck/buggynotes```
2. Install the required dependencies: ```pip install -r requirements.txt```
3. Create a `.env` file in the root directory of the project and add the following line to set the secret key for Django: ```SECRET_KEY='your_secret_key_here'```
4. Collect static files: ```python manage.py collectstatic```
5. Apply the database migrations: ```python manage.py migrate```
6. (Optional) Add demo user accounts with notes for testing: ```python manage.py create_demo_users```
6. Start the Django server: ```python manage.py runserver```

## Usage
After installation, BuggyNotes will be accessible at `http://localhost:8000/` by default.

- **Register**: Create a new user account.
- **Login**: Log in with the user credentials.
- **Create Note**: Add new notes to your account. Notes can be written text or drawn images.
- **View Note**: Edit your existing notes.
- **Backup Notes**: Create and load a backup of your notes.

In the ```example_exploit_payloads``` directory, there are example exploits for all the vulnerabilities in the app.

(Optionally) BuggyNotes comes with two default user accounts pre-created for demonstration purposes:

- **Username**: badpickle
  **Password**: S3r!al!zeM3!

- **Username**: injector
  **Password**: Un10n$elect1

These users already have some example notes added to their accounts, which you can view and interact with upon logging in.

Please use this application in a safe and controlled environment. It is intended for educational purposes to understand and mitigate common web application vulnerabilities.
