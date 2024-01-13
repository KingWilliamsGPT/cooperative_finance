from django.db import models
from members.models import Member
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

ACCOUNT_STATUS_CHOICE = (
        ('Deactivated', 'Deactivated'),
        ('Activated', 'Activated'),
        )

DELETE_STATUS_CHOICE = (
        ('False', 'False'),
        ('True', 'True'),
        )

class ShareAccount(models.Model):
    owner = models.OneToOneField(Member, on_delete=models.CASCADE)
    current_share = models.PositiveIntegerField()
    status = models.CharField(choices=ACCOUNT_STATUS_CHOICE, default='Activated', max_length=11)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.first_name

class ShareBuy(models.Model):
    account = models.ForeignKey(ShareAccount, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    delete_status = models.CharField(choices=DELETE_STATUS_CHOICE, default='False', max_length=5, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account.owner.first_name

class ShareSell(models.Model):
    account = models.ForeignKey(ShareAccount, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    delete_status = models.CharField(choices=DELETE_STATUS_CHOICE, default='False', max_length=5, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account.owner.first_name

@receiver(post_save, sender=Member)
def create_account(sender, **kwargs):
    if kwargs['created']:
        ShareAccount.objects.create(owner=kwargs['instance'],current_share=0)


