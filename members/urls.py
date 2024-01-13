from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (member,member_detail,
                   member_create)

app_name = 'members'
urlpatterns = [
        path('', login_required(member), name='member'),
        path('create/', login_required(member_create), name='create'),
        path('<str:mem_number>/', login_required(member_detail), name='member_detail'),
]
