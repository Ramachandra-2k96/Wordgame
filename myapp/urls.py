from django.urls import path
from .views import login_view, signup_view,chat

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', signup_view, name='signup'),
    path('chat/', chat, name='chat'),
]

