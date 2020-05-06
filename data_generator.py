# generate fake budget data
import random as rdm
import datetime as dt
from decimal import Decimal
from .models import ExpCategory, RevCategory

# CONSTANTS
EXP_CATEGORY = {
    'Food': ["McDonald's", 'Tim Hortons', 'Pizza Pizza', 'The Keg', 'HK Cafe', 'Pho', 'Sushi Bar'],
    'Activities': ['Movie', 'Rec Room', 'Karaoke', 'Pool', 'Escape Room'],
    'Groceries': ['T&T', 'HMart', 'No Frills', 'Sobeys'],
    'Transportation': ['Gas', 'Car Wash', 'Parking'],
    'Softball': ['Team Fee', 'Player Fee'],
    'Sports': ['Badminton', 'Table Tennis', 'Rock Climbing', 'Drop-in'],
    'Travels': ['Trip', 'Food', 'Hotel', 'Airbnb', 'Flight', 'Gas', 'Rental Car'],
    'Equipment': ['WalMart', 'Home Depot', 'Staples', 'IKEA', 'Canadian Tire'],
    'Car Repair': ['Repair', 'Oil Change'],
    'Gym Memberships': ['Gym Membership'],
    'Personal': ['Cell Phone', 'Internet'],
    'Health': ['Dentist', 'Eye Exam', 'Glasses', 'Physio'],
    'Subscriptions': ['Economist', 'MIT Technology Review'],
    'Insurance': ['Car Insurance', 'Home Insurance'],
    'Rent': ['Rent']
}
REV_CATEGORY = {
    'Pay Stub': ['Pay', 'Overtime'],
    'Insurance Claims': ['Dentist', 'Eye Exam', 'Glasses', 'Physio'],
    'Owe Me (Debit)': ['Misc.', 'Softball', 'Meal'],
    'Owe Me (Cash)': ['Misc.', 'Softball', 'Meal'],
    'Refund (Debit)': ['Equipment', 'Activities'],
    'Deposit': ['Deposit'],
    'Withdrawal': ['Withdrawal'],
    'Transfer': ['Transfer']
}
BANK_ACCOUNTS = ['Cash', 'TangoCheq', 'RBCCheq', 'CIBC Cheq', 'TD Savings']
CREDIT_CARDS = ['RBC Avion', 'TangoCC', 'TD Aeroplan Inf', 'CIBC Aventura']
GST = 0.05
# Expenses; LOW: $5-$15; MED: $15-30; HIGH: $30-80
# CASH 0.333 / DEBIT 0.333 / CREDIT 0.333
DAILY_LOW = ['Badminton', 'Table Tennis', 'Drop-in', 'Parking', "McDonald's", 'Tim Hortons', 'Pizza Pizza']

# DEBIT 0.1 / CREDIT 0.9
DAILY_MED = ['Rock Climbing', 'The Keg', 'HK Cafe', 'Pho', 'Sushi Bar', 'Movie', 'Rec Room',
             'Karaoke', 'Pool', 'Escape Room', ]
WEEKLY_LOW = ['Car Wash']
WEEKLY_HIGH = ['T&T', 'HMart', 'No Frills', 'Sobeys', 'Gas']

# CREDIT
MONTHLY_65 = ['Cell Phone', 'Internet', 'Gym Membership']
MONTHLY_HIGH = ['WalMart', 'Home Depot', 'Staples', 'IKEA', 'Canadian Tire', 'Physio']
MONTHLY_250 = ['Car Insurance', 'Home Insurance']
MONTHLY_RENT = ['Rent']

SEASONAL_50 = ['Economist', 'MIT Technology Review', 'Player Fee', 'Oil Change']
SEASONAL_MED = ['Food', 'Gas']
SEASONAL_500 = ['Team Fee', 'Trip', 'Hotel', 'Airbnb', 'Flight', 'Rental Car', 'Repair']

HALF_YEAR_100 = ['Dentist']
TWO_YEAR_100 = ['Eye Exam']
TWO_YEAR_600 = ['Glasses']

# Revenue; LOW: $5-$15; MED: $15-30; HIGH: $30-80
# CASH 0.5 / DEBIT 0.5
DAILY_LOW_R = ['Misc.', 'Softball', 'Meal']

WEEKLY_CASH_FLOW = ['Deposit', 'Withdrawal', 'Transfer']

# DEBIT
BIWEEKLY_2000 = ['Pay']

MONTHLY_300 = ['Overtime']
MONTHLY_MED = ['Physio']

HALF_YEAR_80 = ['Dentist']
TWO_YEAR_80 = ['Eye Exam']
TWO_YEAR_480 = ['Glasses']

ONE_YEAR_HIGH = ['Equipment', 'Activities']

# PAY TYPES:
PAY_TYPE1 = ['cash', 'debit', 'credit']  # EVEN 33.3%
PAY_TYPE2 = ['cash', 'debit']  # EVEN 50%
PAY_TYPE3 = ['debit', 'credit', 'credit', 'credit', 'credit',
             'credit', 'credit', 'credit', 'credit', 'credit']  # SKEWED 1:9 ratio
PAY_TYPE4 = ['credit']
PAY_TYPE5 = ['debit']


# GENERATOR RANDOM INTEGERS WITHIN A RANGE
def generate_integer(level):

    if level == 'LOW':
        return rdm.randint(5, 15)
    elif level == 'MED':
        return rdm.randint(15, 30)
    else:
        return rdm.randint(30, 80)


# GENERATOR FOR OCCURRENCES ON GIVEN FREQUENCY
def generate_occurence(level):

    if level == 'LOW':
        return rdm.randint(0, 2)
    elif level == 'MED':
        return rdm.randint(1, 5)
    else:
        return rdm.randint(3, 8)


# GRAB A RANDOM ITEM FROM LIST
# print(rdm.choice(DAILY_MED))

# Working with dates
start_date = dt.datetime(2020, 1, 1)
# end_date = dt.datetime(2020, 1, 31)
# print(start_date.weekday())  # 0 is Monday
# print(start_date + dt.timedelta(days=1))


# GET EXP/REV CATEGORY
def get_category(cat_type, given_item):

    if cat_type == 'REV':
        dictionary = REV_CATEGORY
    else:
        dictionary = EXP_CATEGORY

    for key, item in dictionary.items():
        if given_item in [n for n in item]:
            return key

    # otherwise...
    return False


# PAY TYPE CARD/BANK SELECTOR
def get_pay_type(pay_type):

    # if debit, select a bank account NOT CASH
    if pay_type == 'debit':
        selected = rdm.choice(BANK_ACCOUNTS[1:])
    # if credit, select a credit card
    elif pay_type == 'credit':
        selected = rdm.choice(CREDIT_CARDS)
    # cash, ignore.
    else:
        selected = None

    return selected


# GENERATE EXPENSE LINE ITEM
def generate_expense(expense_item, price_rate, pay_type_sel, date_stamp):

    item = rdm.choice(expense_item)
    amount = round(generate_integer(price_rate) * (1 + GST), 2)
    category = get_category('EXP', item)
    category_id = list(ExpCategory.objects.filter(name=category).values('id'))[0]['id']
    # category_id = 0  # for testing purposes
    pay_type = rdm.choice(pay_type_sel)
    selected = get_pay_type(pay_type)

    exp_item = dict(
        name=item,
        category=category_id,
        pay_type=pay_type,
        card_name=None,
        bank_account=None,
        date_stamp=format(date_stamp, '%Y-%m-%d'),
        amount=Decimal(amount)
    )
    if pay_type == 'debit':
        exp_item['bank_account'] = selected

        # also need a bank line item

    elif pay_type == 'credit':
        exp_item['card_name'] = selected
    else:
        # cash needs a bank line item


    return exp_item


# GENERATE RANDOM BUDGET DATA!
def generate_budget_data(start_date, end_date):

    on_date = start_date
    while on_date <= end_date:

        # day of month
        day = on_date.day

        # PROCESS DAILY
        num_of_exp = generate_occurence('MED')
        num_of_rev = generate_occurence('LOW')

        for i in range(num_of_exp):
            print(generate_expense(DAILY_LOW, 'LOW', PAY_TYPE1, on_date))

        # increment date
        on_date += dt.timedelta(days=1)

    return True


# generate_budget_data(start_date, end_date)
# print(format(start_date, '%Y-%m-%d'))
