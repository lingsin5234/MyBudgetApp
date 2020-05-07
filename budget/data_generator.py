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
TRANSFER_ACCOUNTS = ['TangoCheq', 'CIBC Cheq', 'TD Savings']
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

# with more Withdrawals
WEEKLY_CASH_FLOW = ['Deposit', 'Withdrawal', 'Withdrawal', 'Withdrawal', 'Transfer', 'Transfer']

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

# IMPORTANT GLOBAL VARIABLES:
rev_pk = 1
exp_pk = 1
bl_pk = 1
cc_pay_pk = 1
cc_line_pk = 1
bank_balances = {1: 500, 2: 5227.84, 5: 24214.15, 4: 11111.34, 3: 25535.13}  # put RBC at the back...
cc_balances = {3: 0, 4: 0, 5: 0, 6: 0}


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
def generate_occurrence(level):

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

    global bl_pk, bank_balances
    line_item = dict(
        model='budget.banklineitem',
        pk=bl_pk,
        fields=dict(
            from_transaction=from_bank,
            to_transaction=to_bank,
            amount=Decimal(amount),
            date_stamp=format(date_stamp, '%Y-%m-%d')
        )
    )

    # update bank balance(s)
    if from_bank is not None:
        bank_balances[from_bank] -= amount
    if to_bank is not None:
        bank_balances[to_bank] += amount

    bl_pk += 1
    return line_item


# GENERATE CREDIT CARD LINE ITEM
def generate_cc_line_item(credit_card, amount, date_stamp):

    global cc_line_pk, cc_balances
    line_item = dict(
        model='budget.creditcardlineitem',
        pk=cc_line_pk,
        fields=dict(
            to_credit_card=credit_card,
            amount=Decimal(amount),
            date_stamp=format(date_stamp, '%Y-%m-%d')
        )
    )

    # update credit card balances
    cc_balances[credit_card] += amount

    cc_line_pk += 1
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

    global exp_pk
    exp_item = dict(
        model='budget.expenselineitem',
        pk=exp_pk,
        fields=dict(
            name=item,
            category=category_id,
            pay_type=pay_type,
            date_stamp=format(date_stamp, '%Y-%m-%d'),
            amount=Decimal(amount)
        )
    )
    exp_pk += 1
    if pay_type == 'debit':
        # get bank/card id
        selected_id = list(BankAccount.objects.filter(nickname=selected).values('id'))[0]['id']
        exp_item['fields']['bank_account'] = selected_id
        exp_item['fields']['card_name'] = None

        # generate bank line item
        bank_item = generate_bank_line_item(selected_id, None, amount, date_stamp)

    elif pay_type == 'credit':
        if item == 'Rent':  # keep bank account fixed for rent
            selected_id = list(CreditCard.objects.filter(nickname='TangoCC').values('id'))[0]['id']
        else:
            selected_id = list(CreditCard.objects.filter(nickname=selected).values('id'))[0]['id']
        exp_item['fields']['bank_account'] = None
        exp_item['fields']['card_name'] = selected_id

        # generate CC item -- keep variable name, for the convenience of the list
        bank_item = generate_cc_line_item(selected_id, amount, date_stamp)
    else:
        exp_item['fields']['bank_account'] = None
        exp_item['fields']['card_name'] = None
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

    global rev_pk
    rev_item = dict(
        model='budget.revenuelineitem',
        pk=rev_pk,
        fields=dict(
            name=item,
            category=category_id,
            cash_debit=pay_type,
            date_stamp=format(date_stamp, '%Y-%m-%d'),
            amount=Decimal(amount)
        )
    )
    rev_pk += 1
    if pay_type == 'debit':
        # get bank/card id
        if item == 'Pay':  # keep bank account fixed for pay
            selected_id = list(BankAccount.objects.filter(nickname='RBCCheq').values('id'))[0]['id']
        else:
            selected_id = list(BankAccount.objects.filter(nickname=selected).values('id'))[0]['id']
        rev_item['fields']['bank_account'] = selected_id

        # generate bank line item
        bank_item = generate_bank_line_item(None, selected_id, amount, date_stamp)

    else:
        rev_item['fields']['bank_account'] = None
        # cash needs a bank line item
        bank_item = generate_bank_line_item(None, 1, amount, date_stamp)

    return [rev_item, bank_item]


# GENERATE RANDOM TRANSFERS BETWEEN ACCOUNTS
def generate_bank_transfers(flow, date_stamp):

    global bank_balances
    rbc_id = list(BankAccount.objects.filter(nickname='RBCCheq').values('id'))[0]['id']
    bank = rdm.choice(TRANSFER_ACCOUNTS)
    bank_id = list(BankAccount.objects.filter(nickname=bank).values('id'))[0]['id']

    if flow == 'FROM RBC':
        amount = rdm.randint(300, 800)
        bank_item = generate_bank_line_item(rbc_id, bank_id, amount, date_stamp)

        # update bank balances
        bank_balances[rbc_id] -= amount
        bank_balances[bank_id] += amount
    else:
        amount = rdm.randint(6000, 10000)
        # check if bank has that much
        escape_counter = 0
        while (bank_balances[bank_id] < amount) and (escape_counter < 10):
            bank = rdm.choice(TRANSFER_ACCOUNTS)
            bank_id = list(BankAccount.objects.filter(nickname=bank).values('id'))[0]['id']
            escape_counter += 1
        if bank_balances[bank_id] < amount:
            amount = 0  # transfer nothing
        bank_item = generate_bank_line_item(bank_id, rbc_id, amount, date_stamp)
        # print('REFRESH RBC:', bank_item)

        # update bank balances
        bank_balances[bank_id] -= amount
        bank_balances[rbc_id] += amount

    # DEBUG
    # print(bank_item, bank_id, rbc_id, date_stamp)

    return [bank_item]


# GENERATE CREDIT CARD PAYMENTS
def generate_cc_payments(date_stamp):

    global bank_balances, cc_balances, cc_pay_pk

    # loop thru and pay off each credit card balance
    payment_list = []
    for cc, cb in cc_balances.items():
        if cb > 0:
            for bnk, bal in bank_balances.items():

                if (bnk != 1) & (bal > cb):  # ignore Cash; pay it off

                    # generate cc payment
                    cc_pay_item = dict(
                        model='budget.creditcardpayment',
                        pk=cc_pay_pk,
                        fields=dict(
                            from_bank=bnk,
                            to_credit_card=cc,
                            amount=cb,
                            date_stamp=format(date_stamp, '%Y-%m-%d')
                        )
                    )

                    # generate bank item as well and add to payment list along with cc_pay_item
                    bank_item = generate_bank_line_item(bnk, None, cb, date_stamp)

                    # use append here cuz we're adding ITEM to the list
                    payment_list.append(cc_pay_item)
                    payment_list.append(bank_item)
                    # extend is extending the list with a list

                    # update the bank balance and cc balance
                    bank_balances[bnk] = bal - cb
                    cc_balances[cc] = 0
                    break

    return payment_list


# GENERATE CASH-BANK TRANSFERS (Withdrawal / Deposit)
def generate_withdraw_deposit(flow, date_stamp):

    global bl_pk, bank_balances
    rbc_id = list(BankAccount.objects.filter(nickname='CIBC Cheq').values('id'))[0]['id']
    cash_id = 1

    if flow == 'Withdrawal':
        from_bank = rbc_id
        to_bank = cash_id
    else:
        from_bank = cash_id
        to_bank = rbc_id

    amount = rdm.randint(50, 200)

    bank_item = dict(
        model='budget.banklineitem',
        pk=bl_pk,
        fields=dict(
            from_transaction=from_bank,
            to_transaction=to_bank,
            amount=Decimal(amount),
            date_stamp=format(date_stamp, '%Y-%m-%d')
        )
    )

    # update bank balances
    bank_balances[from_bank] -= amount
    bank_balances[to_bank] += amount

    return [bank_item]


# GENERATE RANDOM BUDGET DATA!
def generate_budget_data(start_date, end_date):

    output_data = []
    on_date = start_date

    # counters for the processors
    weekly_counter = rdm.randint(0, 6)
    weekly_flag = True
    biweekly_flag = True
    monthly_fixed = [rdm.randint(1, 28), rdm.randint(1, 28), rdm.randint(1, 28)]
    monthly_counter = rdm.randint(1, 28)
    monthly_flag = True
    seasonal_flag = 1
    half_year_flag = 3
    one_year_flag = 5
    two_year_flag = 6
    # print(monthly_counter, monthly_flag)
    while on_date <= end_date:

        # Date Breakdown
        day = on_date.day
        day_of_week = on_date.weekday()
        month = on_date.month

        # ---- DAILY ---- #
        num_of_exp = generate_occurrence('MED')
        for i in range(num_of_exp):
            # print(generate_expense(DAILY_LOW, 'LOW', PAY_TYPE1, on_date))
            output_data.extend(generate_expense(DAILY_LOW, 'LOW', PAY_TYPE1, on_date))

        num_of_exp = generate_occurrence('LOW')
        for i in range(num_of_exp):
            output_data.extend(generate_expense(DAILY_MED, 'MED', PAY_TYPE3, on_date))

        num_of_rev = generate_occurrence('LOW')
        for i in range(num_of_rev):
            # print(generate_revenue(DAILY_LOW_R, 'LOW', PAY_TYPE2, on_date))
            output_data.extend(generate_revenue(DAILY_LOW_R, 'LOW', PAY_TYPE2, on_date))
        # ----------------- #

        # ---- WEEKLY ---- #
        if (day_of_week == weekly_counter) & weekly_flag:
            num_of_exp = generate_occurrence('LOW')
            for i in range(num_of_exp):
                output_data.extend(generate_expense(WEEKLY_LOW, 'LOW', PAY_TYPE3, on_date))

            num_of_exp = generate_occurrence('LOW')
            for i in range(num_of_exp):
                output_data.extend(generate_expense(WEEKLY_HIGH, 'HIGH', PAY_TYPE3, on_date))

            weekly_flag = False  # set weekly flag to not create new weekly_counter until Sunday

        # WEEKLY_CASH_FLOW = ['Deposit', 'Withdrawal', 'Transfer']
        if rdm.randint(0, 1) == 1:
            flow = rdm.choice(WEEKLY_CASH_FLOW)
            if flow == 'Transfer':
                output_data.extend(generate_bank_transfers('FROM RBC', on_date))

            else:
                output_data.extend(generate_withdraw_deposit(flow, on_date))

        # Reset Weekly Counter
        if (day_of_week == 6) & (not weekly_flag):
            weekly_flag = True
            weekly_counter = rdm.randint(0, 6)
            # print('WEEKLY: ', day)
            # print(bank_balances)
            # print(cc_balances)

        # BI-WEEKLY; set to Thursday
        if (day_of_week == 3) & biweekly_flag:
            output_data.extend(generate_revenue(BIWEEKLY_2000, 2000, PAY_TYPE5, on_date))
            biweekly_flag = False
        elif (day_of_week == 3) & (not biweekly_flag):  # set flag for next week
            biweekly_flag = True
        # ----------------- #

        # ---- MONTHLY ---- #
        if day == 1:
            output_data.extend(generate_expense(MONTHLY_RENT, 2000, PAY_TYPE4, on_date))
        if day == monthly_fixed[0]:
            output_data.extend(generate_expense([MONTHLY_65[0]], 50, PAY_TYPE4, on_date))
            output_data.extend(generate_expense([MONTHLY_65[1]], 80, PAY_TYPE4, on_date))
        if day == monthly_fixed[1]:
            output_data.extend(generate_expense([MONTHLY_65[2]], 65, PAY_TYPE4, on_date))
        if day == monthly_fixed[2]:
            output_data.extend(generate_expense([MONTHLY_250[0]], 250, PAY_TYPE4, on_date))
            output_data.extend(generate_expense([MONTHLY_250[1]], 20, PAY_TYPE4, on_date))

        # PAY OFF CREDIT CARD(s)
        if (day == 22) & monthly_flag:
            output_data.extend(generate_cc_payments(on_date))
            # print(type(output_data[len(output_data) - 1]))

        # if monthly_flag (some value between 1 - 28)
        if (day == monthly_counter) & monthly_flag:
            output_data.extend(generate_expense(MONTHLY_HIGH, 'HIGH', PAY_TYPE4, on_date))

            # revenue
            if rdm.randint(0, 1) == 1:
                output_data.extend(generate_revenue(MONTHLY_300, 300, PAY_TYPE5, on_date))
            output_data.extend(generate_revenue(MONTHLY_MED, 100, PAY_TYPE5, on_date))

        if day == 28:  # if last day, then reset flag.
            monthly_flag = False

        # Reset Monthly Counter
        if (day == 28) & (not monthly_flag):
            monthly_flag = True
            monthly_counter = rdm.randint(1, 28)
            print("MONTHLY:", month)
            print(bank_balances)
            print(cc_balances)
        # ----------------- #

        # ---- SEASONAL ---- #
        if seasonal_flag == 3:
            output_data.extend(generate_expense([SEASONAL_50[0]], 50, PAY_TYPE4, on_date))
            output_data.extend(generate_expense([SEASONAL_50[1]], 20, PAY_TYPE4, on_date))
            if rdm.randint(0, 1) == 1:
                output_data.extend(generate_expense([SEASONAL_50[2]], 60, PAY_TYPE4, on_date))
            if rdm.randint(0, 1) == 1:
                output_data.extend(generate_expense([SEASONAL_50[3]], 40, PAY_TYPE4, on_date))
            if rdm.randint(0, 1) == 1:
                output_data.extend(generate_expense(SEASONAL_500, 500, PAY_TYPE4, on_date))

            num_of_exp = generate_occurrence('LOW')
            for i in range(num_of_exp):
                output_data.extend(generate_expense(SEASONAL_MED, 'MED', PAY_TYPE4, on_date))
            seasonal_flag = 0

        if (day == 28) & (seasonal_flag != 3):
            seasonal_flag += 1
        # ----------------- #

        # ---- HALF-YEAR ---- #
        if half_year_flag == 6:
            output_data.extend(generate_expense(HALF_YEAR_100, 100, PAY_TYPE4, on_date))
            output_data.extend(generate_revenue(HALF_YEAR_80, 80, PAY_TYPE5, on_date))
            half_year_flag = 0
        if (day == 24) & (half_year_flag != 6):
            half_year_flag += 1
        # ------------------- #

        # ---- ONE YEAR ---- #
        # random refunds
        if one_year_flag == 12:
            output_data.extend(generate_revenue(ONE_YEAR_HIGH, 'HIGH', PAY_TYPE5, on_date))

            # once a year RBC balance refresh
            output_data.extend(generate_bank_transfers('TO RBC', on_date))
            one_year_flag = 0
        if (day == 20) & (one_year_flag != 12):
            one_year_flag += 1
        # ------------------ #

        # ---- TW0-YEAR ---- #
        if two_year_flag == 24:
            output_data.extend(generate_expense(TWO_YEAR_100, 100, PAY_TYPE4, on_date))
            output_data.extend(generate_revenue(TWO_YEAR_80, 80, PAY_TYPE5, on_date))
            output_data.extend(generate_expense(TWO_YEAR_600, 600, PAY_TYPE4, on_date))
            output_data.extend(generate_revenue(TWO_YEAR_480, 480, PAY_TYPE5, on_date))
            two_year_flag = 0
        if (day == 15) & (two_year_flag != 24):
            two_year_flag += 1
        # ------------------ #

        # increment date
        on_date += dt.timedelta(days=1)
    # print(output_data)
    print("FINAL")
    print(bank_balances)
    print(cc_balances)
    return output_data


# generate_budget_data(start_date, end_date)
# print(format(start_date, '%Y-%m-%d'))
