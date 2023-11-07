from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('note/<int:note_id>/', views.view_note, name='view_note'),
    path('create/', views.create_note, name='create_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note')
]