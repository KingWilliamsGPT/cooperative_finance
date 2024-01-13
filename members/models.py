from django.db import models

# Create your models here.

ACCOUNT_STATUS_CHOICE = (
        ('Deactivated','Deactivated'),
        ('Activated', 'Activated'),
        )

class Member(models.Model):
    mem_number = models.PositiveIntegerField(default=0, blank=False, unique=True, editable=False)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    contact = models.CharField(max_length=10)
    status = models.CharField(choices=ACCOUNT_STATUS_CHOICE, default='Activated', max_length=11,editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        add = not self.pk
        super(Member, self).save(*args, **kwargs)
        if add:
            if self.pk < 10:
                pk = 0 + self.pk
            else:
                pk = self.pk
            self.mem_number = pk
            kwargs["force_insert"] = False
            super(Member, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name

