import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
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
# print(pio.templates)
# '''
# Call Budget
budget_demo = DjangoDash("BudgetDemo")
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# convert all objects from dict_to_model
bank = BankAccount.objects.values_list()
cc = CreditCard.objects.values_list()
bank_line = BankLineItem.objects.values_list().order_by('-date_stamp')
cc_line = CreditCardLineItem.objects.values_list().order_by('-date_stamp')
cc_pay = CreditCardPayment.objects.values_list().order_by('-date_stamp')

# convert columns to lists
bank_col = BankAccount._meta.fields
cc_col = CreditCard._meta.fields
bl_col = BankLineItem._meta.fields
cl_col = CreditCardLineItem._meta.fields
cp_col = CreditCardPayment._meta.fields

# get the data frame
o_dict = pd_reconcile_bank_balances(bank, bank_col, bank_line, bl_col, cc_pay, cp_col)

# construct the graph
fig = go.Figure()

# configure the colours
fig_colours = px.colors.qualitative.Plotly

# plot candlestick plot
for i, b_name in enumerate(o_dict):
    df = o_dict[b_name]
    # print(b_name, df)
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=b_name,
        text=df['transactions'],
        increasing_line_color=fig_colours[5 + i % 5],
        decreasing_line_color=fig_colours[4 - i % 5]
    ))

'''
# scatter + line graph
for i in df.account_name.unique():
    fig.add_trace(go.Scatter(
        x=df[df['account_name'] == i]['date_stamp'],
        y=df[df['account_name'] == i]['amount'],
        text=df[df['account_name'] == i]['Trans_Type'],
        mode='lines+markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name=i
    ))
'''
fig.layout = dict(
        xaxis={'type': 'date', 'title': 'Date'},
        yaxis={'title': 'Spending / Earnings'},
        margin={'l': 40, 'b': 40, 't': 20, 'r': 10},
        legend={'x': 1, 'y': 1},
        hovermode='closest',
        height=750
        # template='plotly_dark'
    )

# show the graph
budget_demo.layout = html.Div([
    dcc.Graph(
        id='budget_demo',
        figure=fig
    )
])

