from django.db import models
from django.contrib.auth.models import User

class ProcessedQuestion(models.Model):
    original_text = models.TextField()
    processed_text = models.TextField()
    language = models.CharField(max_length=10, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.original_text[:50] + "..." if len(self.original_text) > 50 else self.original_text

class QuestionIntent(models.Model):
    processed_question = models.ForeignKey(ProcessedQuestion, on_delete=models.CASCADE, related_name='intents')
    intent_type = models.CharField(max_length=50, choices=[
        ('definition', 'Definition'),
        ('explanation', 'Explanation'),
        ('comparison', 'Comparison'),
        ('example', 'Example'),
        ('unknown', 'Unknown')
    ])
    confidence_score = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.intent_type} ({self.confidence_score})"

class ExtractedEntity(models.Model):
    processed_question = models.ForeignKey(ProcessedQuestion, on_delete=models.CASCADE, related_name='entities')
    entity_text = models.CharField(max_length=200)
    entity_type = models.CharField(max_length=50, choices=[
        ('topic', 'Topic'),
        ('concept', 'Concept'),
        ('person', 'Person'),
        ('date', 'Date'),
        ('other', 'Other')
    ])
    start_position = models.IntegerField()
    end_position = models.IntegerField()
    
    def __str__(self):
        return f"{self.entity_text} ({self.entity_type})"
