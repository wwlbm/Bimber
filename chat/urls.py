from django.urls import path
from chat.views import chat_view, chat_list

app_name = 'chat'

urlpatterns = [
    path('', chat_list, name='chat_list'),
    path('<int:user_id>/', chat_view, name='room'),
]