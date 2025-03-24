import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/covid.csv")
df.dropna(inplace=True)
df['дата'] = pd.to_datetime(df['дата'])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Статистика COVID-19 по регионам России"),
    html.Div([
        dcc.Dropdown(
            id='region-select',
            options=[{'label': r, 'value': r} for r in df['Регион'].unique()],
            value='Республика Бурятия'),
        dcc.DatePickerSingle(
            id='start-date',
            min_date_allowed=df['дата'].min(),
            max_date_allowed=df['дата'].max(),
            initial_visible_month=df['дата'].min(),
            date=df['дата'].min()),
        dcc.DatePickerSingle(
            id='end-date',
            min_date_allowed=df['дата'].min(),
            max_date_allowed=df['дата'].max(),
            initial_visible_month=df['дата'].max(),
            date=df['дата'].max()
        )
    ], style={'padding': 20}),
    html.Div([
        dcc.Graph(id='cases-plot'),
        dcc.Graph(id='deaths-plot'),
    ], style={"display": "flex"}),
])

@app.callback(
    [Output('cases-plot', 'figure'),
     Output('deaths-plot', 'figure')],
    [Input('region-select', 'value'),
     Input('start-date', 'date'),
     Input('end-date', 'date')]
)
def update_plots(region, start_date, end_date):
    filtered = df[(df['Регион'] == region) & (df['дата'] >= pd.to_datetime(start_date)) & (df['дата'] <= pd.to_datetime(end_date))].sort_values('дата')

    cases_fig = px.line(
        filtered,
        x='дата',
        y='случаи заболевания',
        title=f'Заболевания в {region}'
    )

    deaths_fig = px.line(
        filtered,
        x='дата',
        y='количество смертей',
        title=f'Смерти в {region}',
        color_discrete_sequence=['red']
    )

    return cases_fig, deaths_fig

if __name__ == '__main__':
    app.run(debug=True)
