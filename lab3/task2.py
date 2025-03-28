# Импорт необходимых библиотек
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import requests

app = dash.Dash(__name__)


def get_rates(base_currency):
    url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['rates']
    else:
        print(f"Ошибка при получении данных: {response.status_code}")
        return {}


app.layout = html.Div([
    html.H1('Курсы валют и конвертер', style={'textAlign': 'center'}),
    html.Div([
        html.Label('Выберите базовую валюту:'),
        dcc.Dropdown(
            id='base-currency',
            options=[{'label': c, 'value': c} for c in ['USD', 'EUR', 'RUB', 'GBP', 'JPY']],
            value='USD',
            clearable=False
        ),
        dcc.Graph(id='currency-histogram')
    ], style={'padding': 20, 'border': '1px solid #ddd'}),
    html.Div([
        html.H3('Конвертер валют'),
        html.Div([
            dcc.Input(id='amount', type='number', value=1, style={'width': 100}),
            dcc.Dropdown(id='from-currency', style={'width': 100}),
            html.Span('→', style={'fontSize': 24, 'padding': '0 10px'}),
            dcc.Dropdown(id='to-currency', style={'width': 100}),
            html.Div(id='conversion-result')
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': 10})
    ], style={'padding': 20, 'marginTop': 20, 'border': '1px solid #ddd'})
])


@app.callback(
    [Output('currency-histogram', 'figure'),
     Output('from-currency', 'options'),
     Output('to-currency', 'options')],
    Input('base-currency', 'value')
)
def update_data(base_currency):
    rates = get_rates(base_currency)
    df = pd.DataFrame(list(rates.items()), columns=['Валюта', 'Курс'])
    fig = px.bar(
        df,
        x='Валюта',
        y='Курс',
        log_y=True,
        title=f'Курсы валют относительно {base_currency} (логарифмическая шкала)'
    )
    options = [{'label': c, 'value': c} for c in rates.keys()]
    return fig, options, options

@app.callback(
    Output('conversion-result', 'children'),
    [Input('amount', 'value'),
     Input('from-currency', 'value'),
     Input('to-currency', 'value')],
    State('base-currency', 'value')
)
def convert_currency(amount, from_curr, to_curr, base_curr):
    if not all([amount, from_curr, to_curr]):
        return 'Введите параметры'

    rates = get_rates(base_curr)
    try:
        rate = rates[to_curr] / rates[from_curr]
        result = f"{amount:.2f} {from_curr} = {amount * rate:.2f} {to_curr}"
        return html.H4(result, style={'margin': 0})
    except KeyError:
        return 'Ошибка валюты'

if __name__ == '__main__':
    app.run(debug=True)
