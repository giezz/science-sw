import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv"
df = pd.read_csv(url)

delay_columns = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
for col in delay_columns:
    df[col] = df[col].fillna(0)

df['Year'] = df['Year'].astype(int)
df['Month'] = df['Month'].astype(int)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Header([
        html.Center("Анализ задержек авиакомпании"),
        html.Div([
            dcc.Dropdown(
                id='year-selector',
                options=[{'label': str(year), 'value': year} for year in range(2010, 2021)],
                value=2010,
                style={'width': '50%'}
            )
        ]),
    ],
        # style={"position": "fixed", "top": 0, "z-index": 1, "display": "flex"}
    ),
    html.Div([
        html.Div([
            dcc.Graph(id='carrier-delay'),
            dcc.Graph(id='weather-delay'),
        ], style={"display": "flex"}),
        html.Div([
            dcc.Graph(id='nas-delay'),
            dcc.Graph(id='security-delay'),
        ], style={"display": "flex"}),
        dcc.Graph(id='late-aircraft-delay')
    ])
])



@app.callback(
    [Output('carrier-delay', 'figure'),
     Output('weather-delay', 'figure'),
     Output('nas-delay', 'figure'),
     Output('security-delay', 'figure'),
     Output('late-aircraft-delay', 'figure')],
    [Input('year-selector', 'value')]
)
def update_graphs(selected_year):
    filtered_df = df[df['Year'] == selected_year]
    figures = []
    for c in delay_columns:
        monthly_avg = filtered_df.groupby(['Month','Reporting_Airline'])[c].mean().reset_index()
        fig = px.line(
            monthly_avg,
            x='Month',
            y=c,
            color='Reporting_Airline',
            title=f'Среднемесячная задержка: {c}',
            labels={'Month': 'Месяц', c: 'Задержка (минуты)'}
        )
        fig.update_xaxes(tickmode='linear', dtick=1)
        figures.append(fig)

    return figures


if __name__ == '__main__':
    app.run(debug=True)