from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Flashcard, ReviewSession
from .forms import FlashcardForm
import datetime
from django.utils import timezone

@login_required
def create_flashcard(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.owner = request.user
            flashcard.save()
            messages.success(request, 'Flashcard created successfully!')
            return redirect('flashcards:list')
    else:
        form = FlashcardForm()
    return render(request, 'flashcards/create.html', {'form': form})

@login_required
def list_flashcards(request):
    flashcards = Flashcard.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'flashcards/list.html', {'flashcards': flashcards})

@login_required
def review_flashcards(request):
    # Get flashcards that are due for review
    now = timezone.now()
    due_flashcards = Flashcard.objects.filter(
        owner=request.user,
        next_review_date__lte=now
    ).order_by('next_review_date')
    
    if not due_flashcards.exists():
        messages.info(request, 'No flashcards are due for review right now.')
        return render(request, 'flashcards/no_reviews.html')
    
    # Get the first flashcard for review
    flashcard = due_flashcards.first()
    return render(request, 'flashcards/review.html', {'flashcard': flashcard})

@login_required
@require_http_methods(["POST"])
def process_review(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, owner=request.user)
    quality = int(request.POST.get('quality', 0))
    
    # Create a review session
    ReviewSession.objects.create(
        user=request.user,
        flashcard=flashcard,
        quality=quality
    )
    
    # Update flashcard based on spaced repetition algorithm (simplified SM-2)
    if quality < 2:
        # If quality is 'Again' or 'Hard', reset repetition count
        flashcard.repetition_count = 0
        flashcard.interval = 1.0
        if flashcard.ease_factor > 1.3:
            flashcard.ease_factor -= 0.1
    else:
        # If quality is 'Good' or 'Easy'
        flashcard.repetition_count += 1
        if flashcard.repetition_count == 1:
            flashcard.interval = 1.0
        elif flashcard.repetition_count == 2:
            flashcard.interval = 6.0
        else:
            flashcard.interval *= flashcard.ease_factor
            
        if quality == 3:  # 'Easy'
            flashcard.ease_factor += 0.1
    
    # Update next review date
    flashcard.next_review_date = timezone.now() + datetime.timedelta(days=flashcard.interval)
    flashcard.save()
    
    # Check if there are more flashcards to review
    due_flashcards = Flashcard.objects.filter(
        owner=request.user,
        next_review_date__lte=timezone.now()
    ).exclude(id=flashcard_id)
    
    if due_flashcards.exists():
        next_flashcard = due_flashcards.first()
        return JsonResponse({
            'status': 'success',
            'next_flashcard_id': next_flashcard.id,
            'message': 'Review recorded successfully!'
        })
    else:
        return JsonResponse({
            'status': 'completed',
            'message': 'All reviews completed for now!'
        })

@login_required
def edit_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, owner=request.user)
    
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            messages.success(request, 'Flashcard updated successfully!')
            return redirect('flashcards:list')
    else:
        form = FlashcardForm(instance=flashcard)
    
    return render(request, 'flashcards/edit.html', {'form': form, 'flashcard': flashcard})

@login_required
def delete_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, owner=request.user)
    
    if request.method == 'POST':
        flashcard.delete()
        messages.success(request, 'Flashcard deleted successfully!')
        return redirect('flashcards:list')
    
    return render(request, 'flashcards/confirm_delete.html', {'flashcard': flashcard})
