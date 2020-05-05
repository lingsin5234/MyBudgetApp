# this file is to reconcile the bank / cc balances with past transactions
import pandas as pd


# get balances for banks, bank_line_items and credit_card_payments - dictionary version
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
        # print(my_balance)

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

    entire_array = banks_balance

    return entire_array


# get balances for banks, bank_line_items and credit_card_payments - pandas version
def pd_reconcile_bank_balances(banks, bank_col, bank_lines, bl_col, cc_pays, cp_col):

    bank = pd.DataFrame(list(banks), columns=[str(n).replace('budget.BankAccount.', '') for n in bank_col])
    bl = pd.DataFrame(list(bank_lines), columns=[str(n).replace('budget.BankLineItem.', '') for n in bl_col])
    cp = pd.DataFrame(list(cc_pays), columns=[str(n).replace('budget.CreditCardPayment.', '') for n in cp_col])

    # ----- MAP THE BANK ACCOUNTS ----- #
    full_dict = bank.to_dict()
    bank_dict = dict(zip(list(full_dict['id'].values()), list(full_dict['nickname'].values())))
    # print(bank_dict)

    # ----- BANK LINE ITEMS ----- #
    # set Transaction Type
    bl['Trans_Type'] = ''

    # from Cash to Bank ==> a deposit
    deposit_bool = (bl['from_transaction'] == 1) & bl['to_transaction'].notna()
    # print('Deposit:', bl[deposit_bool])
    bl.loc[deposit_bool, 'Trans_Type'] = 'Deposit'

    # from Bank to Cash ==> a Withdrawal
    withdrawal_bool = bl['from_transaction'].notna() & (bl['to_transaction'] == 1)
    # print('Withdrawal:', bl[withdrawal_bool])
    bl.loc[withdrawal_bool, 'Trans_Type'] = 'Withdrawal'

    # from '' to Cash ==> cash received
    cash_rcv_bool = bl['from_transaction'].isna() & (bl['to_transaction'] == 1)
    # print('Cash Received:', bl[cash_rcv_bool])
    bl.loc[cash_rcv_bool,'Trans_Type'] = 'Cash Received'

    # from '' to Bank ==> revenue received
    rev_rcv_bool = bl['from_transaction'].isna() & (bl['to_transaction'] != 1)
    # print('Revenue Received:', bl[rev_rcv_bool])
    bl.loc[rev_rcv_bool, 'Trans_Type'] = 'Revenue Received'

    # transfer between banks
    transfer_bool = [not i for i in (deposit_bool | withdrawal_bool | cash_rcv_bool | rev_rcv_bool)]
    # print('Transfers:', bl[transfer_bool])
    bl.loc[transfer_bool, 'Trans_Type'] = 'Bank Transfer'

    # ----- CREDIT CARD PAYMENTS ----- #
    cp['Trans_Type'] = 'Credit Card Payment'

    # ----- MAP AND ORDER LINE ITEMS ----- #
    # Bank Line Items
    bl.loc[bl['from_transaction'].isna(), 'from_transaction'] = -1
    bl = bl.astype({'from_transaction': 'int64', 'to_transaction': 'int64'})  # convert to int64

    # Add Bank Line Items per Account
    df = bl.loc[bl['from_transaction'] > 0, ['from_transaction', 'Trans_Type', 'amount', 'date_stamp']]\
        .rename(columns={'from_transaction': 'account'})
    df = df.append(bl.loc[bl['to_transaction'] > 0, ['to_transaction', 'Trans_Type', 'amount', 'date_stamp']]
                   .rename(columns={'to_transaction': 'account'}))

    # Credit Card Payments
    df = df.append(cp[['from_bank', 'Trans_Type', 'amount', 'date_stamp']].rename(columns={'from_bank': 'account'}))
    df['account_name'] = df['account'].map(bank_dict)
    # print(df)

    return df
