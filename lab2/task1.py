import pandas as pd
from dash import Dash, html

df = pd.read_csv('../data/airline_data.csv')

app = Dash()

app.layout = [
    html.Header(html.Center(children='Flight Delay Time Statistics')),
    html
]

if __name__ == '__main__':
    app.run()