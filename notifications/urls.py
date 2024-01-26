from django.urls import path

from .views import FetchAllNotifications, FetchUnreadNotifications, MarkAllNotificationsAsRead
from . import views

app_name = 'notifications'

urlpatterns = [
    path('all/', FetchAllNotifications.as_view(), name='list'),
    path('unread/', FetchUnreadNotifications.as_view(), name='unread'),
    path('mark/', MarkAllNotificationsAsRead.as_view(), name='mark'),
    path('reset_last_seen/', views.ResetLastSeen.as_view(), name='reset_last_seen'),
    # non api
    path('<int:pk>/mark_single/', views.MarkNotification.as_view(), name='mark_single'),
]
