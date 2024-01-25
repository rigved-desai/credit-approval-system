from ..models import Customer

def get_customer_by_id(customer_id):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
        return customer
    except: 
        raise
    
def create_customer(customer_details):
    try :
        approved_limit = round(36 * int(customer_details['monthly_income']), -5)
        new_customer = Customer.objects.create(
            first_name=customer_details['first_name'],
            last_name=customer_details['last_name'],
            age=int(customer_details['age']),
            phone_number=customer_details['phone_number'],
            monthly_salary=customer_details['monthly_income'],
            approved_limit=approved_limit
        )
        return new_customer
    except KeyError:
        raise
    except TypeError:
        raise

def update_customer_debt(customer_id, added_debt):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
        current_debt = customer.current_debt
        new_debt = current_debt + added_debt
        Customer.objects.filter(customer_id=customer_id).update(current_debt=new_debt)
    except:
        raise
    