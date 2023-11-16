<h1>BuggyNotes - A Vulnerable Note Taking Web App</h1>

Welcome to the repository of BuggyNotes, the intentionally vulnerable web application made with Django. BuggyNotes is a simple, web-based note-taking application that has been deliberately crafted to include several security vulnerabilities from the OWASP Top 10 (2017).


<summary><h2>About BuggyNotes</h2></summary>

BuggyNotes allows users to create an account, login, and save personal notes. However, due to its intentionally insecure nature, it contains several vulnerabilities.

<details>
<summary>Vulnerabilities</summary>

- **SQL Injection**: The note search function places user supplied text directly in the SQL query without sanitizing it or using a parametrized query, resulting in an SQL injection vulnerability.
- **Broken Access Control**: The user requesting a note is not properly verified to be the note's owner, allowing any authenticated user to view any other users' notes.
- **Cross Site Scripting (XSS)**: User input is not properly validated or escaped, leading to persistent XSS in the note content.
- **Insecure Deserialization**: The `pickle` library is used for serializing and deserializing note backups, which is known to be vulnerable to arbitrary code execution if malicious data is deserialized.
- **XML External Entities (XXE)**: SVG images are parsed using `etree.XMLParser` with default settings, leading to XXE.

</details>

<summary><h2>Installation</h2></summary>

To set up the BuggyNotes, follow these steps:

1. Clone the repository: `git clone https://github.com/Roar1ngDuck/buggynotes`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory of the project and add the following line to set the secret key for Django: `SECRET_KEY='your_secret_key_here'`
4. Collect static files: `python manage.py collectstatic`
5. Apply the database migrations: `python manage.py migrate`
6. (Optional) Add demo user accounts with notes for testing: `python manage.py create_demo_users`
7. Start the Django server: `python manage.py runserver`

<summary><h2>Usage</h2></summary>

After installation, BuggyNotes will be accessible at `http://localhost:8000/` by default.

<details>
<summary>Features</summary>

- **Register**: Create a new user account.
- **Login**: Log in with the user credentials.
- **Create Note**: Add new notes to your account. Notes can be written text or drawn images.
- **View Note**: Edit your existing notes.
- **Backup Notes**: Create and load a backup of your notes.
</details>

In the `example_exploit_payloads` directory, there are example exploits for all the vulnerabilities in the app.

(Optionally) BuggyNotes comes with two default user accounts pre-created for demonstration purposes. These users already have some example notes added to their accounts, which you can view and interact with upon logging in.

<details>
<summary>Accounts</summary>
 <p><strong>Username: </strong>badpickle <strong>Password: </strong>S3r!al!zeM3!</p>
 <p><strong>Username: </strong>injector <strong>Password: </strong>Un10n$elect1</p>
</details>

Please use this application in a safe and controlled environment. It is intended for educational purposes to understand and mitigate common web application vulnerabilities.
