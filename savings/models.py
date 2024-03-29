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

class SavingAccount(models.Model):
    owner = models.OneToOneField(Member, on_delete=models.CASCADE)
    current_balance = models.PositiveIntegerField()
    status = models.CharField(choices=ACCOUNT_STATUS_CHOICE, default='Activated', max_length=11)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-date_created',)
        
    def __str__(self):
        return f'{self.owner.mem_number}'
    
    def is_active(self):
        return self.status == 'Activated'
    

class SavingDeposit(models.Model):
    account = models.ForeignKey(SavingAccount, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=10, decimal_places=2) # monthly savings
    transaction_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True) 
    members_registration_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True) 
    # investment_fund = models.DecimalField(max_digits=10, decimal_places=2)

    delete_status = models.CharField(choices=DELETE_STATUS_CHOICE, default='False', max_length=5, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.account.owner.first_name

class SavingWithdrawal(models.Model):
    account = models.ForeignKey(SavingAccount, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    delete_status = models.CharField(choices=DELETE_STATUS_CHOICE, default='False', max_length=5, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.account.owner.first_name


@receiver(post_save, sender=Member)
def create_account(sender, **kwargs):
    if kwargs['created']:
        SavingAccount.objects.create(owner=kwargs['instance'],current_balance=0)

