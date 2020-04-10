# this file is to reconcile the bank / cc balances with past transactions
import pandas as pd


# get balances for banks, bank_line_items and credit_card_payments
def reconcile_bank_balances(banks, bank_lines, cc_pays, recent_num):

    entire_array = []
    list_of_banks = {}
    banks_balance = {}

    # rename the banks into dictionary by its ID number
    for b in banks:
        id = b['id']
        list_of_banks[id] = b
        banks_balance[id] = []
    # print(list_of_banks[1]['balance'])

    # get all bank lines and cc_pays -- these will already be sorted -date_stamp in views.py
    bank_transactions = []
    for b in bank_lines:

        # from Cash to Bank ==> a deposit
        if b['from_transaction'] == 1 and b['to_transaction'] is not None:
            temp_dict = {
                'bank_id': b['from_transaction'],
                'amount': -b['amount'],
                'date_stamp': b['date_stamp'],
                'trans_type': 'Deposit'
            }
            bank_transactions.append(temp_dict)
            temp_dict = {
                'bank_id': b['to_transaction'],
                'amount': b['amount'],
                'date_stamp': b['date_stamp'],
                'trans_type': 'Deposit'
            }
            bank_transactions.append(temp_dict)

        # from Bank to Cash ==> a Withdrawal
        elif b['from_transaction'] is not None and b['to_transaction'] == 1:
            temp_dict = {
                'bank_id': b['from_transaction'],
                'amount': -b['amount'],
                'date_stamp': b['date_stamp'],
                'trans_type': 'Withdrawal'
            }
            bank_transactions.append(temp_dict)
            temp_dict = {
                'bank_id': b['to_transaction'],
                'amount': b['amount'],
                'date_stamp': b['date_stamp'],
                'trans_type': 'Withdrawal'
            }
            bank_transactions.append(temp_dict)

        # from '' to Cash ==> cash received
        elif b['from_transaction'] is None and b['to_transaction'] == 1:
            temp_dict = {
                'bank_id': b['to_transaction'],
                'amount': b['amount'],
                'date_stamp': b['date_stamp'],
                'trans_type': 'Cash Received'
            }
            bank_transactions.append(temp_dict)

        # from '' to Bank ==> revenue received
        elif b['from_transaction'] is None and b['to_transaction'] != 1:
            temp_dict = {
                'bank_id': b['to_transaction'],
                'amount': b['amount'],
                'date_stamp': b['date_stamp'],
                'trans_type': 'Debit Received'
            }
            bank_transactions.append(temp_dict)

        # transfer between bank accounts
        else:
            temp_dict = {
                'bank_id': b['from_transaction'],
                'amount': -b['amount'],
                'date_stamp': b['date_stamp'],
                'trans_type': 'Bank Transfer'
            }
            bank_transactions.append(temp_dict)
            temp_dict = {
                'bank_id': b['to_transaction'],
                'amount': b['amount'],
                'date_stamp': b['date_stamp'],
                'trans_type': 'Bank Transfer'
            }
            bank_transactions.append(temp_dict)
    for c in cc_pays:
        temp_dict = {
            'bank_id': c['from_bank'],
            'amount': -c['amount'],
            'date_stamp': c['date_stamp'],
            'trans_type': 'Credit Card Payment'
        }
        bank_transactions.append(temp_dict)
    # print(bank_transactions)

    # convert this list of dictionaries into a data_frame, sort date descending
    df = pd.DataFrame.from_dict(bank_transactions).sort_values(by=['date_stamp'], ascending=False)
    # print(df)

    # now for each bank account (incl. cash), re-enact transactions!
    for b in banks_balance:
        # b is the key of list_of_banks and bank_balance dicts
        my_balance = list_of_banks[b]['balance']
        print(my_balance)

        # temp data frame to sort
        temp_df = df[df.bank_id == b].reset_index(drop=True)

        # loop thru to create list of transactions for each bank account
        loop = min(len(temp_df), recent_num)
        for i in range(loop):
            temp_dict = {
                'balance': my_balance - temp_df.loc[i, 'amount'],  # opposite of trans
                'date_stamp': temp_df.loc[i, 'date_stamp'],
                'trans_type': temp_df.loc[i, 'trans_type']
            }
            banks_balance[b].append(temp_dict)
        print(banks_balance)
        break

    return entire_array
