from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .services.customer_services import create_customer
from .services.loan_services import get_loan_by_id, get_loans_by_customer_id, check_loan_eligibility, calculate_correct_interest_rate, calculate_monthly_repayment, create_new_loan

@api_view(['POST'])
def register_user(request):
    customer_details = request.data
    try :
        new_customer = create_customer(customer_details)
        customer_data = {
            "customer_id" : new_customer.customer_id,
            "name" : new_customer.first_name + " " + new_customer.last_name,
            "age" : new_customer.age,
            "approved_limit" : new_customer.approved_limit,
            "phone_number" : new_customer.phone_number
        }
        return Response(customer_data, status=status.HTTP_201_CREATED)
    except (KeyError, TypeError, ValueError):
        return Response({'Error' : "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def check_eligibility(request):
    try: 
        pending_loan_data = request.data
        customer_id = int(pending_loan_data['customer_id'])
        interest_rate = float(pending_loan_data['interest_rate'])
        tenure = int(pending_loan_data['tenure'])
        loan_amount = float(pending_loan_data['loan_amount'])

        is_loan_approved, credit_score = check_loan_eligibility(customer_id)
        corrected_interest_rate = None
        monthly_installment = None
        if is_loan_approved:
            corrected_interest_rate = calculate_correct_interest_rate(interest_rate, credit_score)
            monthly_installment = calculate_monthly_repayment(loan_amount, corrected_interest_rate, tenure)

        loan_approval_data = {
            "customer_id" : customer_id,
            "approval" : is_loan_approved,
            "interest_rate" : interest_rate,
            "corrected_interest_rate": corrected_interest_rate,
            "tenure" : tenure,
            "monthly_installment" : monthly_installment
        }
        return Response(loan_approval_data, status=status.HTTP_200_OK)
    except (KeyError, TypeError, ValueError):
        return Response({'Error' : "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    except: 
        return Response({'Error' : "No customer with given ID found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def create_loan(request):
    try :
        pending_loan_data = request.data
        customer_id = int(pending_loan_data['customer_id'])
        interest_rate = float(pending_loan_data['interest_rate'])
        tenure = int(pending_loan_data['tenure'])
        loan_amount = float(pending_loan_data['loan_amount'])

        is_loan_approved, credit_score = check_loan_eligibility(customer_id)
        corrected_interest_rate = None
        monthly_installment = None
        new_loan = None
        if is_loan_approved:
            corrected_interest_rate = calculate_correct_interest_rate(interest_rate, credit_score)
            monthly_installment = calculate_monthly_repayment(loan_amount, corrected_interest_rate, tenure)
            new_loan = create_new_loan(customer_id, loan_amount, tenure, corrected_interest_rate, monthly_installment)

        data = {
            "loan_id" : new_loan.loan_id if new_loan != None else None,
            "customer_id" : customer_id, 
            "loan_approved" : is_loan_approved,
            "message" : f"Your credit score is {str(credit_score)} which is too low" if not is_loan_approved else None,
            "monthly_installment" : monthly_installment 
        }
        return Response(data, status=status.HTTP_201_CREATED)
    except (KeyError, TypeError, ValueError) :
        return Response({'Error' : "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    except: 
        return Response({'Error' : "No customer with given ID found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def view_loan_by_id(request, loan_id):
    try:
        loan_details = get_loan_by_id(loan_id)
        customer_details = loan_details.customer_id
        loan_data = {
            "loan_id" : loan_details.loan_id,
            "customer" : {
                "customer_id" : customer_details.customer_id,
                "first_name" : customer_details.first_name,
                "last_name" : customer_details.last_name,
                "phone_number" : customer_details.phone_number, 
                "age" : customer_details.age,
            },
            "loan_amount" : loan_details.loan_amount,
            "interest_rate" : loan_details.interest_rate,
            "monthly_installment" : loan_details.monthly_repayment,
            "tenure" : loan_details.tenure
        }
        return Response(loan_data, status=status.HTTP_200_OK)
    except:
        return Response({'Error' : "No loan with given ID found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def view_loans_by_customer_id(request, customer_id):
    try:
        customer_loans = get_loans_by_customer_id(customer_id)
        customer_loans_data = [{
            "loan_id" : loan.loan_id,
            "loan_amount" : loan.loan_amount,
            "interest_rate" : loan.interest_rate,
            "monthly_installment" : loan.monthly_repayment,
            "repayments_left" : loan.tenure - loan.emis_paid_on_time
        } for loan in customer_loans]
        return Response(customer_loans_data, status=status.HTTP_200_OK)
    except: 
        return Response({'Error' : "No customer with given ID found"}, status=status.HTTP_404_NOT_FOUND)
