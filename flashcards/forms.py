from django import forms
from .models import Flashcard

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['question', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
