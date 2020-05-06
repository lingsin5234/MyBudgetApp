# generate fake budget data
import random as rdm
import datetime as dt
from decimal import Decimal
from .models import ExpCategory, RevCategory, BankAccount, CreditCard

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
    elif level == 'HIGH':
        return rdm.randint(30, 80)
    else:
        return level


# GENERATOR FOR OCCURRENCES ON GIVEN FREQUENCY
def generate_occurence(level):

    if level == 'LOW':
        return rdm.randint(0, 2)
    elif level == 'MED':
        return rdm.randint(1, 5)
    elif level == 'HIGH':
        return rdm.randint(3, 8)
    else:
        return level

# GRAB A RANDOM ITEM FROM LIST
# print(rdm.choice(DAILY_MED))

# Working with dates
# start_date = dt.datetime(2020, 1, 1)
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
def get_pay_account(pay_type):

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


# GENERATE BANK LINE ITEM
def generate_bank_line_item(from_bank, to_bank, amount, date_stamp):

    line_item = dict(
        from_transaction=from_bank,
        to_transaction=to_bank,
        amount=Decimal(amount),
        date_stamp=format(date_stamp, '%Y-%m-%d')
    )

    return line_item


# GENERATE EXPENSE LINE ITEM
def generate_expense(expense_item, price_rate, pay_type_sel, date_stamp):

    item = rdm.choice(expense_item)
    amount = round(generate_integer(price_rate) * (1 + GST), 2)
    category = get_category('EXP', item)
    category_id = list(ExpCategory.objects.filter(name=category).values('id'))[0]['id']
    # category_id = 0  # for testing purposes
    pay_type = rdm.choice(pay_type_sel)
    selected = get_pay_account(pay_type)

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
        # get bank/card id
        selected_id = list(BankAccount.objects.filter(nickname=selected).values('id'))[0]['id']
        exp_item['bank_account'] = selected_id

        # generate bank line item
        bank_item = generate_bank_line_item(selected_id, None, amount, date_stamp)

    elif pay_type == 'credit':
        exp_item['card_name'] = selected
        bank_item = None
    else:
        # cash needs a bank line item
        bank_item = generate_bank_line_item(1, None, amount, date_stamp)

    return [exp_item, bank_item]


# GENERATE REVENUE LINE ITEM
def generate_revenue(revenue_item, price_rate, pay_type_sel, date_stamp):

    item = rdm.choice(revenue_item)
    amount = round(generate_integer(price_rate) * (1 + GST), 2)
    category = get_category('REV', item)
    category_id = list(RevCategory.objects.filter(name=category).values('id'))[0]['id']
    # category_id = 0  # for testing purposes
    pay_type = rdm.choice(pay_type_sel)
    selected = get_pay_account(pay_type)

    rev_item = dict(
        name=item,
        category=category_id,
        cash_debit=pay_type,
        bank_account=None,
        date_stamp=format(date_stamp, '%Y-%m-%d'),
        amount=Decimal(amount)
    )
    if pay_type == 'debit':
        # get bank/card id
        if item == 'Pay':  # keep bank account fixed for pay
            selected_id = list(BankAccount.objects.filter(nickname='RBCCheq').values('id'))[0]['id']
        else:
            selected_id = list(BankAccount.objects.filter(nickname=selected).values('id'))[0]['id']
        rev_item['bank_account'] = selected_id

        # generate bank line item
        bank_item = generate_bank_line_item(None, selected_id, amount, date_stamp)

    else:
        # cash needs a bank line item
        bank_item = generate_bank_line_item(None, 1, amount, date_stamp)

    return [rev_item, bank_item]


# GENERATE RANDOM BUDGET DATA!
def generate_budget_data(start_date, end_date):

    output_data = []
    on_date = start_date

    # counters for the processors
    weekly_counter = rdm.randint(0, 6)
    weekly_flag = True
    biweekly_flag = True

    while on_date <= end_date:

        # Date Breakdown
        day = on_date.day
        day_of_week = on_date.weekday()

        # PROCESS DAILY
        num_of_exp = generate_occurence('MED')
        for i in range(num_of_exp):
            # print(generate_expense(DAILY_LOW, 'LOW', PAY_TYPE1, on_date))
            output_data.extend(generate_expense(DAILY_LOW, 'LOW', PAY_TYPE1, on_date))

        num_of_exp = generate_occurence('LOW')
        for i in range(num_of_exp):
            output_data.extend(generate_expense(DAILY_MED, 'MED', PAY_TYPE3, on_date))

        num_of_rev = generate_occurence('LOW')
        for i in range(num_of_rev):
            # print(generate_revenue(DAILY_LOW_R, 'LOW', PAY_TYPE2, on_date))
            output_data.extend(generate_revenue(DAILY_LOW_R, 'LOW', PAY_TYPE2, on_date))

        # PROCESS WEEKLY
        if day_of_week == weekly_counter & weekly_flag:
            num_of_exp = generate_occurence('LOW')
            for i in range(num_of_exp):
                output_data.extend(generate_expense(WEEKLY_LOW, 'LOW', PAY_TYPE3, on_date))
            num_of_exp = generate_occurence('LOW')
            for i in range(num_of_exp):
                output_data.extend(generate_expense(WEEKLY_HIGH, 'HIGH', PAY_TYPE3, on_date))
            weekly_flag = False  # set weekly flag to not create new weekly_counter until Sunday

        # WEEKLY_CASH_FLOW = ['Deposit', 'Withdrawal', 'Transfer']

        # Reset Weekly Counter
        if day_of_week == 6 & (not weekly_flag):
            weekly_flag = True
            weekly_counter = rdm.randint(0, 6)

        # BI-WEEKLY; set to Thursday
        if day_of_week == 3 & biweekly_flag:
            output_data.extend(generate_revenue(BIWEEKLY_2000, 2000, PAY_TYPE5, on_date))
            biweekly_flag = False
        elif day_of_week == 3 & (not biweekly_flag):  # set flag for next week
            biweekly_flag = True

        # MONTHLY

        # increment date
        on_date += dt.timedelta(days=1)
    print(output_data)
    return True


# generate_budget_data(start_date, end_date)
# print(format(start_date, '%Y-%m-%d'))
