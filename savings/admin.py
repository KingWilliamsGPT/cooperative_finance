from django.contrib import admin
from .models import (SavingAccount,SavingDeposit,
                    SavingWithdrawal,)

# Register your models here.
admin.site.register(SavingAccount)
admin.site.register(SavingDeposit)
admin.site.register(SavingWithdrawal)
