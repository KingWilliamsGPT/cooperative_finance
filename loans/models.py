from django.db import models
from members.models import Member
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

STATUS_CHOICE = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        )

ACCOUNT_STATUS_CHOICE = (
       	('Deactivated', 'Deactivated'),
        ('Activated', 'Activated'),
        )

DELETE_STATUS_CHOICE = (
        ('False', 'False'),
        ('True', 'True'),
        )

class LoanAccount(models.Model):
    owner = models.OneToOneField(Member, on_delete=models.CASCADE)
    total_principal = models.PositiveIntegerField()
    status = models.CharField(choices=ACCOUNT_STATUS_CHOICE, default='Activated', max_length=11)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.first_name

    def is_active(self):
        return self.status == 'Activated'
    

class LoanIssue(models.Model):
    account = models.ForeignKey(LoanAccount, on_delete=models.CASCADE)
    loan_num = models.CharField(unique=True, max_length=255, editable=False, default="")
    principal = models.PositiveIntegerField()
    status = models.CharField(choices=STATUS_CHOICE, default='Pending', max_length=15)
    delete_status = models.CharField(choices=DELETE_STATUS_CHOICE, default='False', max_length=5, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)

    def save(self, *args, **kwargs):
        add = not self.pk
        super(LoanIssue, self).save(*args, **kwargs)
        if add:
            date = self.date_created.strftime("%y%m%d")
            if self.pk < 10:
                pk = "0" + str(self.pk)
            else:
                pk = str(self.pk)
            self.loan_num = date + pk
            kwargs["force_insert"] = False
            super(LoanIssue, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.account.owner.first_name} for {self.principal}'


class LoanPayment(models.Model):
    loan_num = models.ForeignKey(LoanIssue, on_delete=models.CASCADE)
    principal = models.PositiveIntegerField()
    delete_status = models.CharField(choices=DELETE_STATUS_CHOICE, default='False', max_length=5, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f'{self.loan_num.account.owner.first_name} for {self.principal}'


class LoansIssue(models.Model):
    account = models.ForeignKey(LoanAccount, on_delete=models.CASCADE)
    loan_num = models.CharField(unique=True, max_length=255)
    principal = models.PositiveIntegerField()
    delete_status = models.CharField(choices=DELETE_STATUS_CHOICE, default='False', max_length=5, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.account.owner.first_name} for {self.principal}'


    class Meta:
        ordering = ('-date_created',)
        verbose_name_plural = "Loans issued"


@receiver(post_save, sender=Member)
def create_account(sender, **kwargs):
    if kwargs['created']:
        LoanAccount.objects.create(owner=kwargs['instance'],total_principal=0)


