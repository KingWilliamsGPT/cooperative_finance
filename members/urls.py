from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (member,member_detail,
                   member_create)
from . import views

app_name = 'members'
urlpatterns = [
        path('', login_required(member), name='member'),
        path('create/', login_required(member_create), name='create'),
        path('<str:mem_number>/', login_required(member_detail), name='member_detail'),
        path('<int:pk>/profile_pic/', login_required(views.UpdateProfilePic.as_view()), name='update_profile_pic'),
]
