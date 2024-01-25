from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(unique=True, primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    age = models.PositiveIntegerField()
    phone_number = models.TextField()
    monthly_salary = models.PositiveBigIntegerField()
    approved_limit = models.PositiveBigIntegerField()
    current_debt = models.BigIntegerField(default=0)

class Loan(models.Model):
    customer_id = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    loan_id = models.AutoField(primary_key=True, unique=True)
    loan_amount = models.FloatField()
    tenure = models.PositiveIntegerField()
    interest_rate = models.FloatField()
    monthly_repayment = models.FloatField() 
    emis_paid_on_time = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()