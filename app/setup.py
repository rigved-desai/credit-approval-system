import pandas as pd
import os
import django

customer_data_path = './data/customer_data.xlsx'
loan_data_path = './data/loan_data.xlsx'

customer_data = pd.read_excel(customer_data_path)
loan_data = pd.read_excel(loan_data_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from api.models import Customer, Loan

for index, row in customer_data.iterrows():
    Customer.objects.create(
        first_name=row['First Name'],
        last_name=row['Last Name'],
        age=row['Age'],
        phone_number=row['Phone Number'],
        monthly_salary=row['Monthly Salary'],
        approved_limit=row['Approved Limit']
    )

for index, row in loan_data.iterrows():
    customer = Customer.objects.get(customer_id=row['Customer ID'])
    loan = Loan.objects.create(
        customer_id=customer,
        loan_id=row['Loan ID'],
        loan_amount=row['Loan Amount'],
        tenure=row['Tenure'],
        interest_rate=row['Interest Rate'],
        monthly_repayment=row['Monthly payment'],
        emis_paid_on_time=row['EMIs paid on Time'],
        start_date=row['Date of Approval'],
        end_date=row['End Date']
    )
    Customer.objects.filter(customer_id=customer.customer_id).update(current_debt=(loan.tenure - loan.emis_paid_on_time) * loan.monthly_repayment)  
    