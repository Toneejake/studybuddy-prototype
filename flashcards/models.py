from django.db import models
from django.contrib.auth.models import User
import datetime

class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcards')
    
    # Spaced repetition fields
    interval = models.FloatField(default=1.0)  # Days until next review
    ease_factor = models.FloatField(default=2.5)  # Ease factor for SM-2 algorithm
    repetition_count = models.IntegerField(default=0)  # Number of times reviewed
    next_review_date = models.DateTimeField(default=datetime.datetime.now)
    
    def __str__(self):
        return self.question[:50] + "..." if len(self.question) > 50 else self.question

class ReviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    review_date = models.DateTimeField(auto_now_add=True)
    quality = models.IntegerField(choices=[
        (0, 'Again'),
        (1, 'Hard'),
        (2, 'Good'),
        (3, 'Easy')
    ])
    
    def __str__(self):
        return f"{self.user.username} - {self.flashcard.question[:30]}... - {self.get_quality_display()}"
