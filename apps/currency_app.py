import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
import requests
import dash
import plotly.express as px
import pandas as pd
from tools import df, transco_dic, transco
import dash_table

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
                        value=["CAD", "EUR", "GBP"],
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

alerte = html.Div([dbc.Alert("Please select at least one currency", color="primary")],
                  style={'display': 'none'}, id="output")


carte_1 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Value for 1 USD dollar", className="card-title"),
                html.Div(form),
                html.Div(dcc.Graph(id='graph-with-control',
                                   config={
                                       'displayModeBar': False
                                   })),
                alerte,
                html.Span(
                    f"Dernière données au {df.date.max().date()}. ",
                    className="card-text",
                ),
                html.A(href="https://exchangeratesapi.io/",
                       target="_blank", children=html.Span("Voir la source"))
                # dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ], className="shadow", style={"border": "none"}
)


layout = dbc.Container([
    carte_1,
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
                  template="simple_white"
                  )
    fig.update_layout(transition_duration=500)
    return fig, {'display': display_alert}


if __name__ == '__main__':
    app.run_server(debug=True)
