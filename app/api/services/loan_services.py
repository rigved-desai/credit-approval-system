from ..models import Loan
from .customer_services import get_customer_by_id, update_customer_debt
from datetime import date, timedelta

def create_new_loan(customer_id, loan_amount, tenure, interest_rate, monthly_payment):
    try :
        start_date = date.today()
        end_date = start_date + timedelta(days=30 * tenure)
        customer = get_customer_by_id(customer_id)
        new_loan = Loan.objects.create(
            customer_id=customer,
            loan_amount=loan_amount,
            tenure=tenure,
            interest_rate=interest_rate,
            monthly_repayment=monthly_payment,
            emis_paid_on_time=0,
            start_date=start_date,
            end_date=end_date
        )    
        added_debt = new_loan.monthly_repayment * new_loan.tenure
        update_customer_debt(customer_id, added_debt)
        return new_loan
    except: 
        raise

def get_loan_by_id(loan_id):
    try:
        loan = Loan.objects.get(loan_id=loan_id)
        return loan
    except:
        raise 

def get_loans_by_customer_id(customer_id):
    try:
        customer_loans = Loan.objects.filter(customer_id=customer_id)
        return customer_loans
    except:
        raise

def check_loan_eligibility(customer_id):
    try :
        customer = get_customer_by_id(customer_id)
        customer_loans = get_loans_by_customer_id(customer_id)
        customer_credit_score = calculate_credit_score(customer_loans, customer)
    
        if customer_credit_score < 10:
            return False, customer_credit_score
        else:
            return True, customer_credit_score
    except:
        raise
    
def calculate_monthly_repayment(loan_amount, interest_rate, tenure):
    monthly_interest_rate = interest_rate/12
    monthly_repayment =  (loan_amount * (monthly_interest_rate/100) * (1 + (monthly_interest_rate/100)) ** tenure) / ((1 + (monthly_interest_rate/100)) ** tenure - 1)
    return monthly_repayment

def calculate_correct_interest_rate(interest_rate, credit_score):
    corrected_interest_rate = None
    if credit_score < 30:
        corrected_interest_rate = max(16.0, interest_rate)
    
    elif credit_score < 50:
        corrected_interest_rate = max(12.0, interest_rate)
    
    elif credit_score >= 50:
        corrected_interest_rate = interest_rate

    return corrected_interest_rate

def calculate_credit_score(customer_loans, customer):
    credit_score = 0
    date_today = date.today()
    sum_of_current_loan_amounts = sum(loan.loan_amount for loan in customer_loans if loan.end_date > date_today)
    sum_of_current_emis = sum(loan.monthly_repayment for loan in customer_loans if loan.end_date > date_today)
    if sum_of_current_loan_amounts >= customer.approved_limit or sum_of_current_emis >= customer.monthly_salary * 0.5:
        return 0

    # Taking in account number of EMIs customer has paid on time till now
    sum_of_all_emi_tenures = sum(loan.tenure for loan in customer_loans)
    sum_of_emis_paid_on_time = sum(loan.emis_paid_on_time for loan in customer_loans)
    if sum_of_all_emi_tenures != 0:
        credit_score += sum_of_emis_paid_on_time/sum_of_all_emi_tenures * 25
    else:
        credit_score += 25

    #Taking in account how many loans are still not paid off completely by customer 
    date_today = date.today()
    total_loans_pending_today = len([loan for loan in customer_loans if loan.end_date >= date_today])
    total_loans = len(customer_loans)
    if total_loans != 0:
        credit_score += (1 - total_loans_pending_today/total_loans) * 25
    else:
        credit_score += 25

    return credit_score


