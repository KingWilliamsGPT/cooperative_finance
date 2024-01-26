from django.db import models
from django.contrib.auth.models import AbstractUser


import notifications.models
import cooperative_finance.settings as settings


class User(AbstractUser):
    # email = None
    notification_last_check_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'User'
    

    def get_latest_notifications(self):
        return notifications.models.Notification.objects.get_unseen_notifications(self)

    def get_last_notifications(self):
        return self.notifications.all()[:settings.DASHBOARD_NOTIFICATION_SIZE]

