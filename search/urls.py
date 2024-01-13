from django.urls import path
from django.contrib.auth.decorators import login_required


from .views import (search,member_result,
                    loan_result,)

app_name = "search"
urlpatterns = [
        path('', login_required(search), name='search'),
        path('members/result', login_required(member_result), name='member_results'),
        path('loans/result', login_required(loan_result), name='loan_results'),
]
