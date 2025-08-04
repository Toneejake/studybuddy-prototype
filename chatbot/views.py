from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Conversation, Message
from .forms import MessageForm
from nlp.services import process_question, generate_response

@login_required
def conversations_list(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'chatbot/conversations.html', {'conversations': conversations})

@login_required
def create_conversation(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'New Conversation')
        conversation = Conversation.objects.create(
            user=request.user,
            title=title
        )
        return redirect('chatbot:conversation_detail', conversation_id=conversation.id)
    
    return render(request, 'chatbot/create_conversation.html')

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Save user message
            user_message = form.save(commit=False)
            user_message.conversation = conversation
            user_message.sender = 'user'
            user_message.save()
            
            # Process the question and generate response
            user_text = user_message.content
            processed_data = process_question(user_text, request.user)
            bot_response = generate_response(processed_data, user_text)
            
            # Save bot response
            bot_message = Message.objects.create(
                conversation=conversation,
                sender='bot',
                content=bot_response
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'user_message': user_message.content,
                    'bot_response': bot_response
                })
            
            return redirect('chatbot:conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    messages_list = conversation.messages.all().order_by('timestamp')
    return render(request, 'chatbot/conversation.html', {
        'conversation': conversation,
        'messages': messages_list,
        'form': form
    })

@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    
    if request.method == 'POST':
        conversation.delete()
        messages.success(request, 'Conversation deleted successfully!')
        return redirect('chatbot:conversations')
    
    return render(request, 'chatbot/confirm_delete.html', {'conversation': conversation})

@login_required
def quick_chat(request):
    """Quick chat without creating a conversation"""
    if request.method == 'POST':
        question = request.POST.get('question', '')
        if question:
            processed_data = process_question(question, request.user)
            response = generate_response(processed_data, question)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'response': response
                })
            
            return render(request, 'chatbot/quick_chat.html', {
                'question': question,
                'response': response
            })
    
    return render(request, 'chatbot/quick_chat.html')
