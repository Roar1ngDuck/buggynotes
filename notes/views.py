from django.http import HttpResponse
from .models import Note
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
import pickle

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

def backup_notes(request):
    # Make sure this view is only accessible by a POST request
    if request.method == 'POST':
        # Query all notes for the current user (assuming there is a user field in Note model)
        notes = Note.objects.filter(owner=request.user)
        
        # Serialize the notes with pickle
        serialized_notes = pickle.dumps(list(notes.values()))

        # Create an HTTP response with the pickled data as an attachment
        response = HttpResponse(serialized_notes, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="notes_backup.bak"'

        return response
    else:
        # If not a POST request, redirect to the home page or handle as necessary
        return redirect('/')
    
def load_backup(request):
    if request.method == 'POST':
        # Get the uploaded file
        backup_file = request.FILES.get('backup_file')
        
        if backup_file:
            # Deserialize the notes from the uploaded file
            notes_data = pickle.load(backup_file)

            for note_data in notes_data:
                print(note_data)
                # Create new Note instances or update existing ones
                unique = {'id': note_data['id']}
                Note.objects.update_or_create(defaults=note_data, **unique)
            messages.success(request, 'Backup loaded successfully.')
        else:
            messages.error(request, 'No file was uploaded.')

        return redirect('index')
    else:
        # Redirect to home if not a POST request
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