from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from notes.models import Note

class Command(BaseCommand):
    help = 'Create demo user accounts'

    def handle(self, *args, **kwargs):
        demo_users = [
            ('badpickle', 'S3r!al!zeM3!', [
{'title': 'Serialization formats', 'content': 
""" - JSON
 - XML
 - YAML
 - BSON
 - Pickle""", 'is_drawn': 0},
                {'title': 'Git Commands Quick Reference', 'content': 
"""'git status' to check the status of your changes.
'git add .' to stage all your changes for commit.
'git commit -m "Commit message"' to commit your staged changes with a message.
'git push origin main' to push your commits to the main branch on the remote repository.
'git pull' to update your local repository with the latest changes from remote.""", 'is_drawn': 0},
            ]),
            ('injector', 'Un10n$elect1', [
                {'title': 'Common SQL Queries Cheat Sheet', 'content': 
"""SELECT * FROM table_name; - Retrieves everything from a table.
SELECT column1, column2 FROM table_name; - Retrieves specific columns from a table.
SELECT * FROM table_name WHERE condition; - Retrieves data under a certain condition.
INSERT INTO table_name (column1, column2) VALUES (value1, value2); - Inserts new data into a table.
UPDATE table_name SET column1 = value1 WHERE condition; - Updates data in a table.
DELETE FROM table_name WHERE condition; - Deletes data from a table.""", 'is_drawn': 0},
{'title': 'Python Web Frameworks', 'content': 
""" - Django
 - Flask
 - Pyramid
 - Web2py
 - Tornado""", 'is_drawn': 0},
            ]),
        ]

        for username, password, notes in demo_users:
            try:
                user, created = User.objects.get_or_create(username=username, defaults={'password': password})
                if created:
                    user.set_password(password)  # Ensure the password is hashed
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully created user {username}'))
                    
                    # Create notes for the user
                    for note_info in notes:
                        Note.objects.create(owner=user, **note_info)
                    self.stdout.write(self.style.SUCCESS(f'Successfully created notes for user {username}'))

                else:
                    self.stdout.write(self.style.WARNING(f'User {username} already exists. Skipping.'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Error creating user {username}: {str(e)}'))
