from tools import human_format
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from .components import ModernCard
import pandas as pd
import plotly.express as px
import yfinance as yf
import datetime
from .components import ModernCard


# on initialise un premier df qui contient la valeur par défaut
valeur_a_initialiser = ["AMZN", "GOOGL", "MSFT", "AAPL"]
dico_df = {}
for i, m in enumerate(valeur_a_initialiser):
    stock = yf.Ticker(m)
    if i == 0:
        df = stock.history(period="max")[["Close"]]
        df.rename(columns={"Close": m}, inplace=True)
    else:
        temp = stock.history(period="max")[["Close"]]
        temp.rename(columns={"Close": m}, inplace=True)
        df = df.merge(temp, left_index=True, right_index=True, how="left")
df['Date'] = df.index


# selector data
url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed-symbols_csv/data/595a1f263719c09a8a0b4a64f17112c6/nasdaq-listed-symbols_csv.csv"
listing = pd.read_csv(url)
listing.rename(columns={"Symbol": "value",
                        "Company Name": "label"}, inplace=True)


# selector
selector1 = dcc.Dropdown(
    options=listing.to_dict("records"),
    multi=True,
    value="AMZN",
    id="selected_companies"
)

# slider
year_min = df.Date.dt.year.min()
year_max = df.Date.dt.year.max()

slider1 = dcc.RangeSlider(
    marks={f"{i}": f"{i}" for i in range(year_min, 2021)},
    min=year_min,
    max=year_max,
    value=[2016, 2020],
    id="selected_years",
)

# graphique
chart = dcc.Graph(id="main_chart",
                  config={
                      'displayModeBar': False
                  })


# layout
layout = html.Div([selector1, ModernCard(
    [chart, slider1], style={"margin-top": "30px"})])


# callback
@ app.callback(
    Output('main_chart', 'figure'),
    [Input('selected_companies', 'value'),
     Input('selected_years', 'value')
     ],
)
def update_figure(selected_companies, selected_years):
    global df
    if type(selected_companies) != type([]):
        selected_companies = [selected_companies]
    for company in selected_companies:
        if company not in df.columns:
            stock = yf.Ticker(company)
            temp = stock.history(period="max")[["Close"]]
            temp.rename(columns={"Close": company}, inplace=True)
            df = df.merge(temp, left_index=True, right_index=True, how="left")
    df['Date'] = df.index
    df.Date = pd.to_datetime(df.Date)
    df2 = df.melt(id_vars=["Date"])
    df2.rename(columns={"value": "Close", "variable": "Company"}, inplace=True)
    df3 = df2[(df2.Company.isin(selected_companies))
              & (df2.Date.dt.year > selected_years[0])
              & (df2.Date.dt.year < selected_years[1])
              ]
    fig = px.line(df3, x="Date", y="Close", color="Company")
    return fig
