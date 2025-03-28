# Импорт необходимых библиотек
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
df = pd.read_csv(url)

app = dash.Dash(__name__)

launch_sites = df['Launch Site'].unique().tolist()
launch_sites_options = [{'label': 'Все стартовые комплексы', 'value': 'All'}]
launch_sites_options += [{'label': site, 'value': site} for site in launch_sites]

payload_min = df['Payload Mass (kg)'].min()
payload_max = df['Payload Mass (kg)'].max()

app.layout = html.Div([
    html.H1('Анализ запусков SpaceX',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(
        id='site-dropdown',
        options=launch_sites_options,
        value='All',
        placeholder="Выберите стартовый комплекс",
        searchable=True
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Диапазон полезной нагрузки (кг):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=payload_min,
        max=payload_max,
        step=1000,
        marks={i: str(i) for i in range(int(payload_min), int(payload_max) + 1000, 2000)},
        value=[payload_min, payload_max]
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'All':
        fig = px.pie(
            df,
            names='Launch Site',
            values='class',
            title='Успешные запуски по всем стартовым комплексам'
        )
    else:
        filtered_df = df[df['Launch Site'] == selected_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Успешные запуски для комплекса {selected_site}',
            labels={'0': 'Неудача', '1': 'Успех'}
        )
    return fig


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = df[(df['Payload Mass (kg)'] >= low) & (df['Payload Mass (kg)'] <= high)]

    if selected_site != 'All':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.strip(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version',
        stripmode='overlay',
        title='Зависимость успешности запуска от полезной нагрузки',
        labels={'class': 'Результат запуска'},
        category_orders={'class': [0, 1]}
    )
    fig.update_yaxes(tickvals=[0, 1], ticktext=['Неудача', 'Успех'])
    return fig


if __name__ == '__main__':
    app.run(debug=True)
