from django.contrib import admin
from .models import (IncomeType,Income,
                    ExpenseType,Expense)

# Register your models here.

admin.site.register(IncomeType)
admin.site.register(Income)
admin.site.register(ExpenseType)
admin.site.register(Expense)
