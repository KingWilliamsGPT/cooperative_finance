from django.conf import settings
from django.db import models
from django.db.models.manager import Manager


# class Notification(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     is_read = models.BooleanField(default=False)
#     content = models.TextField()
#     type = models.CharField(max_length=100, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'User:{self.user} / Type:{self.type}'


class NotificiationManager(Manager):
    def get_unseen_notifications(self, user):
        last_check = user.notification_last_check_time
        if last_check:
            return user.notifications.filter(date_created__gt=last_check).filter(is_read=False)
        return user.notifications.filter(is_read=False)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False, blank=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000, blank=True)
    redirect_url = models.CharField(blank=True, max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    icon = models.ImageField(blank=True, null=True)

    # manager
    objects = NotificiationManager()

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f'Notification(user:{self.user} tag:{self.tag})'



# class Tag(models.Model):
#     name = models.CharField(max_length=100)
#     icon = models.ImageField(blank=True, null=True)


#     def __str__(self):
#         return f'Tag(name:{self.name})'


