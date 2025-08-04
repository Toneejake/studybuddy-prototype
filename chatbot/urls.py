from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.conversations_list, name='conversations'),
    path('create/', views.create_conversation, name='create_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('quick/', views.quick_chat, name='quick_chat'),
]
