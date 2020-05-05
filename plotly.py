import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from django.forms.models import model_to_dict
from .models import BankAccount, BankLineItem, CreditCard, CreditCardLineItem, CreditCardPayment
from .reconcile import pd_reconcile_bank_balances

from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

'''
# SIMPLE EXAMPLE app
app = DjangoDash("SimpleExample", external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')


app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                dict(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
'''

'''
# Call Budget
budget_demo = DjangoDash("BudgetDemo", external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# convert all objects from dict_to_model
bank = BankAccount.objects.all()
cc = CreditCard.objects.all()
bank_line = BankLineItem.objects.all().order_by('-date_stamp')
cc_line = CreditCardLineItem.objects.all().order_by('-date_stamp')
cc_pay = CreditCardPayment.objects.all().order_by('-date_stamp')

banks = []
ccs = []
bank_lines = []
cc_lines = []
cc_pays = []

for b in bank:
    add = model_to_dict(b)
    banks.append(add)
for c in cc:
    add = model_to_dict(c)
    ccs.append(add)
for bl in bank_line:
    add = model_to_dict(bl)
    bank_lines.append(add)
for cl in cc_line:
    add = model_to_dict(cl)
    cc_lines.append(add)
for cp in cc_pay:
    add = model_to_dict(cp)
    cc_pays.append(add)

# recapture the previous values
# print("Views output: ", reconcile_bank_balances(banks, bank_lines, cc_pays, 10))
balances = pd_reconcile_bank_balances(banks, bank_lines, cc_pays)

#  df = pd.DataFrame.from_dict(bank_lines)
print(balances)

budget_demo.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                dict(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])
'''
