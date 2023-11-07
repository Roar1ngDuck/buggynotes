from django.http import HttpResponse
from .models import Note
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, get_object_or_404, render
from django.template import Context, Template
from django.utils.safestring import mark_safe

@login_required
def index(request):
    notes = request.user.notes.all()
    
    return render(request, "notes/index.html", {'notes': notes})

@login_required
def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id) # The owner of the note is not checked here, creating a case of broken access control
    #note = get_object_or_404(Note, id=note_id, owner=request.user)  # Ensure the note belongs to the logged-in user

    if request.method == 'POST':
        # Update note with form data
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        # Redirect to note listing view after saving
        return redirect('index')
    else:
        return render(request, 'notes/view_note.html', {'note': note})

@login_required
def create_note(request):
    if request.method == 'POST':
        # Create a new blank Note object and save it.
        new_note = Note(owner=request.user)
        new_note.save()
        # Redirect to the edit page for the new note.
        return redirect('view_note', new_note.id)
    else:
        # If someone tries to access this URL with GET, redirect them to the index page.
        return redirect('index')

@login_required
def delete_note(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id, owner=request.user)  # Ensure the note belongs to the logged-in user
        note.delete()
        return redirect('index')
    else:
        # If someone tries to access this URL with GET, redirect them to the index page.
        return redirect('index')

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