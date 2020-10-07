from tools import human_format
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from .components import ModernCard


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
    dbc.Label("Région", className="font-weight-bold"),
    dcc.Dropdown(
        options=[{"label": "ALL", "value": "ALL"}] + [{"label": m,
                                                       "value": m} for m in superstore2.Region.unique()],
        value="ALL",
        multi=False,
        id="region-control"
    )
])


product_category = dbc.FormGroup([
    dbc.Label("Catégorie", className="font-weight-bold"),
    dcc.Dropdown(
        options=[{"label": "ALL", "value": "ALL"}] + [{"label": m,
                                                       "value": m} for m in superstore2["Product Category"].unique()],
        value="ALL",
        multi=False,
        id="category-control"
    )
])


customer_segment = dbc.FormGroup([
    dbc.Label("Customer Segment", className="font-weight-bold"),
    dcc.Checklist(
        options=[{"label": m, "value": m}
                 for m in superstore["Customer Segment"].unique()],
        value=superstore["Customer Segment"].unique(),
        id="customer-segment-control",
        labelStyle={'display': 'block'}

    )
])


form = html.Div(
    [region,
     product_category,
     customer_segment]
)


ligne_indicateurs = dbc.Row(
    [dbc.Col(ModernCard(
        dbc.CardBody([
            html.H6("West"),
            html.H1(id="west-card"),
        ], style={"color": color_map['West']})
    )),
        dbc.Col(ModernCard(
            dbc.CardBody([
                html.H6("South"),
                html.H1(id="south-card"),
            ], style={"color": color_map['South']}
            )
        )), dbc.Col(ModernCard(
            dbc.CardBody([
                    html.H6("Central"),
                    html.H1(id="central-card"),
                    ],
                style={"color": color_map['Central']})
        )), dbc.Col(ModernCard(
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


# graphique de gauche
sales_chart_left = dcc.Graph(id="sales_chart_left_big",
                             config={
                                 'displayModeBar': False
                             })

sales_chart_col = dbc.Col(
    ModernCard(
        dbc.CardBody([
            html.Div(sales_chart_left),
        ])
    ),
    width=12
)

# graphique top par category
top_products = superstore2.groupby("Product Sub-Category")['Sales'].agg(
    sum).reset_index().sort_values("Sales", ascending=False).head(5)
fig = px.bar(top_products, y="Product Sub-Category",
             x="Sales", orientation='h')
# fig.update_yaxes(autorange="reversed")
fig.update_layout(showlegend=False)

sales_chart_right = dcc.Graph(id="sales_chart_rigth",
                              figure=fig,
                              config={
                                 'displayModeBar': False
                              })

top_n_col = dbc.Col(
    ModernCard(
        dbc.CardBody([
            html.Div(sales_chart_right),
        ])
    ),
    width=6
)

# graphique carte


# layout

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(form, width=2),
                dbc.Col(
                    [
                        ligne_indicateurs,
                        dbc.Row([sales_chart_col], style={
                                "margin-top": "30px"}),
                        dbc.Row([top_n_col], style={
                                "margin-top": "30px"})
                    ]
                ),
            ]
        ),

    ]
)


@ app.callback(
    [Output('sales_chart_left_big', 'figure'),
     Output('west-card', 'children'),
     Output('south-card', 'children'),
     Output('central-card', 'children'),
     Output('east-card', 'children'),

     ],
    [Input('region-control', 'value'),
     Input('category-control', 'value'),
     Input('customer-segment-control', 'value'),
     ]
)
def update_figure(selected_region,  category, customer_segment):
    filtered = superstore2
    # filtre région
    if selected_region == "ALL" or selected_region is None:
        pass
    else:
        filtered = filtered[filtered.Region == selected_region]
    # filtre catégorie
    if category in superstore2["Product Category"].unique():
        filtered = filtered[filtered["Product Category"] == category]
    # filtre customer_segment
    filtered = filtered[filtered["Customer Segment"].isin(customer_segment)]
    # graphique 1
    base_graph = filtered.groupby(['Order Date', 'Region'])[
        'Sales'].agg(sum).reset_index()
    fig = px.line(base_graph, x="Order Date", y="Sales", color="Region",
                  template="simple_white",
                  color_discrete_map=color_map
                  )
    # chiffres du haut
    West = human_format(
        filtered[filtered.Region == "West"]['Sales'].sum())
    South = human_format(
        filtered[filtered.Region == "South"]['Sales'].sum())
    Central = human_format(
        filtered[filtered.Region == "Central"]['Sales'].sum())
    East = human_format(
        filtered[filtered.Region == "East"]['Sales'].sum())
    return fig, West, South, Central, East
