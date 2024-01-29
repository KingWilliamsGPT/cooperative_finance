from django.db import models

# Create your models here.

ACCOUNT_STATUS_CHOICE = (
        ('Deactivated','Deactivated'),
        ('Activated', 'Activated'),
        )

def _trim_name(s):
    s = s.strip()
    if s:
        s = s.split(maxsplit=1)[0]
    return s

class Member(models.Model):
    mem_number = models.PositiveIntegerField(default=0, blank=False, unique=True, editable=False)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    middle_name = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256)
    contact = models.CharField(max_length=20)
    status = models.CharField(choices=ACCOUNT_STATUS_CHOICE, default='Activated', max_length=11,editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(upload_to='members/profile_pic', blank=True, null=True)

    def save(self, *args, **kwargs):
        add = not self.pk
        super(Member, self).save(*args, **kwargs)
        
        self.first_name = _trim_name(self.first_name)
        self.last_name = _trim_name(self.last_name)
        self.middle_name = _trim_name(self.middle_name)

        if add:
            if self.pk < 100:
                self.mem_number = 100 + self.pk
            kwargs["force_insert"] = False
            super(Member, self).save(*args, **kwargs)
        
        super().save()

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f'{self.first_name} {self.last_name} {self.middle_name}'

