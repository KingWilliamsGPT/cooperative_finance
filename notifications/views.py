from typing import Any
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from django.views import View
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


# helper

def reset_notification_last_seen(user):
    user.notification_last_check_time = timezone.now()
    user.save()

def index(request):
    return render(request, 'notifications_index.html')


class FetchUnreadNotifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FetchAllNotifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkAllNotificationsAsRead(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        Notification.objects.filter(user=request.user).update(is_read=True)
        return Response(status=status.HTTP_200_OK)


class ResetLastSeen(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        reset_notification_last_seen(request.user)
        return Response(status=status.HTTP_200_OK)


class MarkNotification(View):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # mark the notifcation
        notification = get_object_or_404(Notification, pk=pk)
        if notification.user != request.user:
            raise Http404('this notification does not exits')
        notification.is_read = True
        notification.save()

        request.user.notification_last_check_time = timezone.now()
        request.user.save()
        return HttpResponseRedirect(notification.redirect_url or '/')