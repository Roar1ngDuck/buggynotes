from django.shortcuts import render
from django.http import HttpResponse
from .models import Note
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

@login_required
def index(request):
    notes = [
    Note(id=1, title="Grocery List", content="Milk, Eggs, Bread, Butter, Apples"),
    Note(id=2, title="Workout Routine", content="Monday: Chest\nTuesday: Back\nWednesday: Rest\nThursday: Arms\nFriday: Legs"),
    Note(id=3, title="Book Recommendations", content="1. '1984' by George Orwell\n2. 'To Kill a Mockingbird' by Harper Lee\n3. 'The Great Gatsby' by F. Scott Fitzgerald")
]

    return render(request, "notes/index.html", {'notes': notes})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')  # Redirect to login page after signup
    template_name = 'registration/signup.html'  # Path to the signup template

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid