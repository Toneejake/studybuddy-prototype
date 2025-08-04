from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('', views.list_flashcards, name='list'),
    path('create/', views.create_flashcard, name='create'),
    path('review/', views.review_flashcards, name='review'),
    path('review/<int:flashcard_id>/process/', views.process_review, name='process_review'),
    path('edit/<int:flashcard_id>/', views.edit_flashcard, name='edit'),
    path('delete/<int:flashcard_id>/', views.delete_flashcard, name='delete'),
]
