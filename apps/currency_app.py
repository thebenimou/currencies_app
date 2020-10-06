import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app


import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


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
            lg=4, sm=12
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
            lg=8, sm=12

        ),
    ],
)


layout = dbc.Container([
    # html.H3("Currency App"),
    html.H1("Currency App", className="bd-title",
            style={"margin-bottom": "30px"}),
    # html.Hr(),
    form,
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='graph-with-control',
                              config={
                                  'displayModeBar': False
                              })),
        ],
        align="center",
    ),
    html.Div(
        dbc.Alert(f"Dernière données au {df.date.max().date()}", color="secondary")),
    html.Div([dbc.Alert("Please select at least one currency", color="primary")],
             style={'display': 'none'}, id="output"),
],

    fluid=True
)


@ app.callback(
    [Output('graph-with-control', 'figure'),
     Output(component_id='output', component_property='style')],
    [Input('currency-control', 'value'), Input('year-control', 'value')])
def update_figure(selected_currency, year_range):
    display_alert = "none"
    if type(selected_currency) != type([]):
        selected_currency = [selected_currency]
    if selected_currency == []:
        selected_currency = ["EUR"]
        display_alert = "block"
    filtered_df = df[(df.currency.isin(selected_currency))
                     & (df.year >= year_range[0]) & (df.year <= year_range[1])]
    fig = px.line(filtered_df, x="date", y="value", color='currency',
                  template="simple_white",
                  )
    fig.update_layout(transition_duration=500)
    return fig, {'display': display_alert}


if __name__ == '__main__':
    app.run_server(debug=True)
