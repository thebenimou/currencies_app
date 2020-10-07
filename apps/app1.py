from tools import human_format
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app


import pandas as pd
import pandas as pd
import plotly.express as px
superstore = pd.read_excel(
    "https://sds-platform-private.s3-us-east-2.amazonaws.com/uploads/P1-SuperStoreUS-2015.xlsx")
us_cities = pd.read_csv("us-zip-code-latitude-and-longitude.csv", sep=";")
pd.options.display.max_columns = 100
superstore2 = superstore.merge(us_cities.drop(
    "City", 1), left_on="Postal Code", right_on="Zip")


color_map = {
    "West": "#0FA3B1",
    "East": "#502419",
    "Central": "#C0DFA1",
    "South": "#0A2463"}

region = dbc.FormGroup([
    dbc.Label("Région"),
    dcc.Dropdown(
        options=[{"label": "ALL", "value": "ALL"}] + [{"label": m,
                                                       "value": m} for m in superstore2.Region.unique()],
        value="ALL",
        multi=False,
        id="region-control"
    )
])


product_category = dbc.FormGroup([
    dbc.Label("Catégorie"),
    dcc.Dropdown(
        options=[{"label": "ALL", "value": "ALL"}] + [{"label": m,
                                                       "value": m} for m in superstore2["Product Category"].unique()],
        value="ALL",
        multi=False,
        id="category-control"
    )
])


view = dbc.FormGroup([
    dbc.Label("View"),
    dcc.RadioItems(
        options=[
            {'label': 'Region', 'value': 'sales'},
            {'label': 'Categorie', 'value': 'product_categories'},
        ],
        value='sales',
        id="view-control",
        labelStyle={'display': 'block'}
    )])

form = html.Div(
    [region,
     product_category,
     view]
)


ligne_indicateurs = dbc.Row(
    [dbc.Col(dbc.Card(
        dbc.CardBody([
            html.H6("West"),
            html.H1(id="west-card"),
        ], style={"color": color_map['West']})
    )),
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H6("South"),
                html.H1(id="south-card"),
            ], style={"color": color_map['South']}
            )
        )), dbc.Col(dbc.Card(
            dbc.CardBody([
                    html.H6("Central"),
                    html.H1(id="central-card"),
                    ],
                style={"color": color_map['Central']})
        )), dbc.Col(dbc.Card(
            dbc.CardBody([
                    html.H6("East"),
                    html.H1(id="east-card"),
                    ], style={"color": color_map['East']})
        )), ]
)
# layout = html.Div(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(
#                     form, width=2
#                 ),
#                 dbc.Col(
#                     [
#                         dbc.Row(ligne_indicateurs),
#                         dbc.Row(dcc.Graph(id="sales_chart"))
#                     ]
#                 ),
#             ],
#         ),
#     ]
# )

chart = dcc.Graph(id="sales_chart",
                  config={
                      'displayModeBar': False
                  })

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(form, width=2),
                dbc.Col(
                    [
                        ligne_indicateurs,
                        dbc.Row(dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    # html.H6("South"),
                                    html.Div(chart),
                                ]), style={"margin-top": "30px"}
                            ),
                            width=12
                        ))
                    ]
                ),
            ]
        ),

    ]
)


@ app.callback(
    [Output('sales_chart', 'figure'),
     Output('west-card', 'children'),
     Output('south-card', 'children'),
     Output('central-card', 'children'),
     Output('east-card', 'children'),

     ],
    [Input('region-control', 'value'),
     Input('view-control', 'value'),
     Input('category-control', 'value'),

     ]
)
def update_figure(selected_region, view, category):
    # filtre région
    if selected_region == "ALL" or selected_region is None:
        filtered = superstore2
    else:
        filtered = superstore2[superstore2.Region == selected_region]
    # filtre catégorie
    if category in superstore2["Product Category"].unique():
        filtered = superstore2[superstore2["Product Category"] == category]
    # vue 1
    if view == "sales":
        filtered2 = filtered.groupby(['Order Date', 'Region'])[
            'Sales'].agg(sum).reset_index()
        fig = px.line(filtered2, x="Order Date", y="Sales", color="Region",
                      template="simple_white",
                      color_discrete_map=color_map)
    if view == "product_categories":
        filtered2 = filtered.groupby(['Order Date', 'Product Category'])[
            'Sales'].agg(sum).reset_index()
        fig = px.line(filtered2, x="Order Date",
                      template="simple_white",
                      y="Sales", color="Product Category")
    fig.update_layout(transition_duration=500)
    West = human_format(
        filtered[filtered.Region == "West"]['Sales'].sum())
    South = human_format(
        filtered[filtered.Region == "South"]['Sales'].sum())
    Central = human_format(
        filtered[filtered.Region == "Central"]['Sales'].sum())
    East = human_format(
        filtered[filtered.Region == "East"]['Sales'].sum())

    return fig, West, South, Central, East
