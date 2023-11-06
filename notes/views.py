from django.shortcuts import render
from django.http import HttpResponse
from .models import Note

def index(request):
    notes = [
    Note(id=1, title="Grocery List", content="Milk, Eggs, Bread, Butter, Apples"),
    Note(id=2, title="Workout Routine", content="Monday: Chest\nTuesday: Back\nWednesday: Rest\nThursday: Arms\nFriday: Legs"),
    Note(id=3, title="Book Recommendations", content="1. '1984' by George Orwell\n2. 'To Kill a Mockingbird' by Harper Lee\n3. 'The Great Gatsby' by F. Scott Fitzgerald")
]

    return render(request, "notes/index.html", {'notes': notes})

