import pandas as pd
from dash import Dash, html
import plotly.express as px

df = pd.read_csv('../data/airline_data.csv')

app = Dash()

avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
weather_figure = px.line(avg_weather, x='Month', y='WeatherDelay',
                         color='Reporting_Airline',
                         title='Average weather delay time (minutes) by airline')

app.layout = [
    html.Header(html.Center(children='Flight Delay Time Statistics')),
    html.Div(
        children=[
            html.Div(),
            html.Div(),
            html.Div()
        ]
    )
]

if __name__ == '__main__':
    app.run(port=8080)
