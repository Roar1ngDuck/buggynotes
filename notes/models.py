from django.db import models
from django.conf import settings

class Note(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # User model configured for the project.
        on_delete=models.CASCADE,  # CASCADE means that if the user is deleted, all their notes are also deleted.
        related_name='notes'  # This allows access to a user's notes with user.notes.all()
    )
    title = models.CharField(max_length=200)
    content = models.TextField()

    