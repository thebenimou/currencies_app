import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

# get data

url = "https://api.exchangeratesapi.io/history?start_at=1999-01-01&end_at=2020-12-02&base=USD"
resp = requests.get(url)
dico = resp.json()
df = pd.DataFrame.from_records(dico['rates']).transpose()
df['date'] = df.index
df['date'] = pd.to_datetime(df['date'])
df = df.melt(id_vars=df.columns[-1])
df.rename(columns={"variable": "currency"}, inplace=True)
df['year'] = df['date'].apply(lambda x: x.year)

transco = pd.read_csv("transco.csv", sep=";")
transco.index = transco["abbr"]
transco_dic = transco.to_dict()['label']

# on filtre que là où la transco est dispo
df = df[df.currency.isin(list(transco_dic.keys()))]

selected_currency = ["CAD"]
# fig = px.line(df[[selected_currency, "date"]],
#               x="date", y="CAD", title='CAD for 1 USD')
filtered_df = df[df.currency.isin(selected_currency)]
fig = px.line(filtered_df, x="date", y="value", color='currency')


form = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Currency"),
                    dcc.Dropdown(
                        options=[
                            {"label": transco_dic[m], "value": m} for m in df.currency.unique()
                        ],
                        value='CAD',
                        id='currency-control',
                        multi=True
                    ),
                ]
            ),
            width=4,
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Year Range"),
                    dcc.RangeSlider(
                        id='year-control',
                        min=df.year.min(),
                        max=df.year.max(),
                        step=1,
                        value=[2013, 2020],
                        marks={str(year): str(year)
                               for year in range(df.year.min(), df.year.max(), 2)}
                    ),
                ]
            ),
            width=8,
        ),
    ],
)

app.layout = dbc.Container([
    html.H1("Currency App"),
    html.Hr(),
    form,
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='graph-with-control')),
        ],
        align="center",
    ),
    html.Div([dbc.Alert("This is a primary alert", color="primary")],
             style={'display': 'block'})
],
)


@app.callback(
    Output('graph-with-control', 'figure'),
    [Input('currency-control', 'value'), Input('year-control', 'value')])
def update_figure(selected_currency, year_range):
    if type(selected_currency) != type([]):
        selected_currency = [selected_currency]
    if selected_currency == []:
        selected_currency = ["EUR"]
    filtered_df = df[(df.currency.isin(selected_currency))
                     & (df.year >= year_range[0]) & (df.year <= year_range[1])]
    fig = px.line(filtered_df, x="date", y="value", color='currency')
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
