# this file is to reconcile the bank / cc balances with past transactions
import numpy as np
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
    bank_names = list(full_dict['nickname'].values())
    bank_dict = dict(zip(list(full_dict['id'].values()), bank_names))
    bal_dict = dict(zip(list(full_dict['nickname'].values()), list(full_dict['balance'].values())))
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
    cp['amount'] = -cp['amount']  # make payments negative

    # ----- MAP AND ORDER LINE ITEMS ----- #
    # Bank Line Items
    bl.loc[bl['from_transaction'].isna(), 'from_transaction'] = -1
    bl.loc[bl['to_transaction'].isna(), 'to_transaction'] = -1
    bl = bl.astype({'from_transaction': 'int64', 'to_transaction': 'int64'})  # convert to int64

    # Add Bank Line Items per Account
    df = bl.loc[bl['from_transaction'] > 0, ['from_transaction', 'Trans_Type', 'amount', 'date_stamp']]\
        .rename(columns={'from_transaction': 'account'})
    df['amount'] = -df['amount']  # make these negative only
    df = df.append(bl.loc[bl['to_transaction'] > 0, ['to_transaction', 'Trans_Type', 'amount', 'date_stamp']]
                   .rename(columns={'to_transaction': 'account'}))

    # Credit Card Payments
    df = df.append(cp[['from_bank', 'Trans_Type', 'amount', 'date_stamp']].rename(columns={'from_bank': 'account'}))

    # Assign Bank Account Names
    df['account_name'] = df['account'].map(bank_dict)

    # ----- REORDER AND GET BALANCES ----- #
    df.sort_values(by='date_stamp', axis=0, ascending=False, inplace=True)

    # create large data transaction table
    cdf = df[['account_name', 'date_stamp', 'amount']].groupby(['date_stamp', 'account_name'], as_index=False).sum()
    cdf = cdf.merge(df[['account_name', 'date_stamp', 'Trans_Type']]
                    .groupby(['date_stamp', 'account_name'], as_index=False)['Trans_Type']
                    .apply(lambda x: ','.join(x)).reset_index(), on=['account_name', 'date_stamp'])\
        .rename(columns={0: 'transactions'})

    # create candle df and add columns
    candle_df = []
    cdf['Open'], cdf['Low'], cdf['High'], cdf['Close'] = [0, 0, 0, 0]
    rv_bank_names = []
    for i, x in enumerate(bank_names):
        if len(cdf.loc[cdf['account_name'] == x]) > 0:
            temp_df = cdf.loc[cdf['account_name'] == x,
                              ['date_stamp', 'amount', 'transactions', 'Open', 'Low', 'High', 'Close']]\
                .set_index('date_stamp').sort_index(ascending=False)

            # work backwards with current balance as 'Close'; minus rolling (expanding)
            dates = temp_df.index
            temp_df['minus_expanding'] = -temp_df['amount'].expanding(2).sum()
            temp_df['Open'] = float(bal_dict[x]) + temp_df['minus_expanding']
            temp_df['Close'] = temp_df['Open'] + [float(n) for n in temp_df['amount']]

            # fix first items NAN
            temp_df.loc[dates[0], 'Close'] = float(bal_dict[x])
            temp_df.loc[dates[0], 'Open'] = temp_df.loc[dates[0], 'Close'] - float(temp_df.loc[dates[0], 'amount'])

            # high and lows
            temp_df['High'] = temp_df.apply(lambda x: max(x['Open'], x['Close']), axis=1)
            temp_df['Low'] = temp_df.apply(lambda x: min(x['Open'], x['Close']), axis=1)

            # print(x, bal_dict[x], temp_df)
            rv_bank_names.append(x)
            candle_df.append(temp_df)

    # concat
    cdf = pd.concat(candle_df, axis=1, keys=rv_bank_names)

    # send out as a list
    list_df = []
    for x in rv_bank_names:
        if len(cdf[x]) > 0:
            # print(x, cdf[x][['transactions', 'Open', 'Low', 'High', 'Close']])
            list_df.append(cdf[x][['transactions', 'Open', 'Low', 'High', 'Close']])

    output_dict = dict(zip(rv_bank_names, list_df))

    return output_dict
