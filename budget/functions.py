# custom functions listed in this file
from .models import BankAccount, RevCategory


# get bank line item form data from the revenue line item input
def get_rev_data(post_data):
    # get some objects to input correct reference
    withdrawal = RevCategory.objects.get(name="Withdrawal")
    deposit = RevCategory.objects.get(name="Deposit")
    cash = BankAccount.objects.get(nickname="Cash")

    # if Withdrawal:
    if post_data['category'] == str(withdrawal.id):
        rev_data = {
            'amount': post_data['amount'],
            'from_transaction': post_data['bank_account'],
            'to_transaction': str(cash.id),
            'date_stamp': post_data['date_stamp']
        }
    # if Deposit:
    elif post_data['category'] == str(deposit.id):
        rev_data = {
            'amount': post_data['amount'],
            'from_transaction': str(cash.id),
            'to_transaction': post_data['bank_account'],
            'date_stamp': post_data['date_stamp']
        }
    else:
        rev_data = {
            'amount': post_data['amount'],
            'from_transaction': '',
            'to_transaction': post_data['bank_account'],
            'date_stamp': post_data['date_stamp']
        }
    return rev_data


# get bank line item form data from the expense line item input
def get_exp_data(post_data):
    exp_data = {
        'amount': post_data['amount'],
        'from_transaction': '',
        'to_transaction': post_data['credit_card'],
        'date_stamp': post_data['date_stamp']
    }
    return exp_data


# update the bank accounts based the bank line item!
def update_bank_rev(data):
    cash = BankAccount.objects.get(nickname="Cash")

    # from Cash to Bank ==> a deposit
    if data['from_transaction'] == str(cash.id) and not(data['to_transaction'] == ''):
        bank = BankAccount.objects.get(id=int(data['to_transaction']))
        bank.balance += float(data['amount'])
        cash.balance -= float(data['amount'])
        bank.save()
        cash.save()

    # from Bank to Cash ==> a Withdrawal
    elif not(data['from_transaction'] == '') and data['to_transaction'] == str(cash.id):
        bank = BankAccount.objects.get(id=int(data['from_transaction']))
        bank.balance -= float(data['amount'])
        bank.save()

    # from '' to Cash ==> cash received
    elif data['from_transaction'] == '' and data['to_transaction'] == str(cash.id):
        cash.balance += float(data['amount'])
        cash.save()

    # actual revenue item to bank account
    else:
        bank = BankAccount.objects.get(id=int(data['to_transaction']))
        bank.balance += float(data['amount'])
        bank.save()

    return
