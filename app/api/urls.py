from django.urls import path
from .views import register_user, view_loan_by_id, view_loans_by_customer_id, check_eligibility, create_loan

urlpatterns = [
    path('register', register_user, name='register-user'),
    path('view-loan/<loan_id>', view_loan_by_id, name = 'view-loan'),
    path('view-loans/<customer_id>', view_loans_by_customer_id, name='view-customer-loans'),
    path('check-eligibility', check_eligibility, name='check-loan-eligibilty'),
    path('create-loan', create_loan, name='create-loan')
]