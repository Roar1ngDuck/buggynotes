from django.http import HttpResponse
from .models import Note
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, get_object_or_404, render
from .helpers import sanitize_svg, optimize_svg
from django.db import connection
import pickle
import json

@login_required
def index(request):
    # Retrieve the search term from the POST request
    search_term = request.POST.get('search', '')

    # Direct SQL query without parameterized inputs, leading to SQL injection vulnerability
    raw_query = f"SELECT * FROM notes_note WHERE owner_id = {request.user.id} AND content LIKE '%{search_term}%'"
    notes = connection.cursor().execute(raw_query).fetchall()

    # Convert raw query results into a list of dictionaries to match the note model
    notes = [
        {'id': row[0], 'title': row[1], 'content': row[2], 'is_drawn': row[4]}
        for row in notes
    ]

    # This is the proper way to do a search without an SQL injection vulnerability, since Djangos built in ORM methods are safe. 
    # An alternative is to use a parameterized query.
    # notes = request.user.notes.all().filter(content__icontains=search_term)
    
    return render(request, "notes/index.html", {'notes': notes})

@login_required
def view_note(request, note_id, is_drawn):
    note = get_object_or_404(Note, id=note_id) # The owner of the note is not checked here, creating a case of broken access control
    #note = get_object_or_404(Note, id=note_id, owner=request.user)  # Ensure the note belongs to the logged-in user

    if request.method == 'POST':
        # Update note with form data
        note.title = request.POST.get('title')
        content = request.POST.get('content')
        if is_drawn == 1:
            # The 'sanitize_svg' function will sanitize the given SVG file by having a whitelist of permitted XML properties. 
            # Without sanitizing, even if the XXE vulnerability in 'optimize_svg' is fixed, there will still be a XSS vulnerability here.
            # content = sanitize_svg(content)
            content = optimize_svg(content)

        note.content = content
        note.is_drawn = is_drawn
        note.save()
        # Redirect to note listing view after saving
        return redirect('index')
    else:
        return render(request, 'notes/view_note.html', {'note': note})
    
@login_required
def create_note(request, is_drawn):
    # Make sure this view is only accessible by a POST request
    if request.method == 'POST':
        # Create a new blank Note object and save it.
        new_note = Note(owner=request.user)
        new_note.is_drawn = is_drawn
        if is_drawn == 1:
            new_note.content = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="SVG" xml:space="preserve"></svg>"""
        new_note.save()
        # Redirect to the edit page for the new note.
        return redirect('view_note', new_note.id, is_drawn)
    
    return redirect('index')
    
@login_required
def delete_note(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id, owner=request.user)  # Ensure the note belongs to the logged-in user
        note.delete()
    
    return redirect('index')

@login_required
def backup_notes(request):
    # Make sure this view is only accessible by a POST request
    if request.method == 'POST':
        # Query all notes for the current user
        notes = request.user.notes.all()

        # Serialize the notes with pickle. Using pickle leads to an insecure deserialization vulnerability in 'load_backup'.
        serialized_notes = pickle.dumps(list(notes.values()))
        #serialized_notes = json.dumps(list(notes.values())) # Python json module is secure by default

        # Create an HTTP response with the pickled data as an attachment
        response = HttpResponse(serialized_notes, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="notes_backup.bak"'

        return response
    
    return redirect('/')
    
@login_required
def load_backup(request):
    if request.method == 'POST':
        # Get the uploaded file
        backup_file = request.FILES.get('backup_file')
        
        if backup_file:
            # Deserialize the notes from the uploaded file. Unpickling malicious data causes arbitrary code execution.
            # This can be fixed by using a secure alternative unpickling library, or by using the standard python json module, which is secure by default.
            notes_data = pickle.load(backup_file)
            #notes_data = json.load(backup_file) #  # Python json module is secure by default

            for note_data in notes_data:
                # Create new Note instances or update existing ones
                unique = {'id': note_data['id']}
                note_data["content"] = sanitize_svg(note_data["content"])
                Note.objects.update_or_create(defaults=note_data, **unique)
    
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