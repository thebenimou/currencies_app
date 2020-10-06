import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, currency_app


# menu
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
sidebar = html.Div(
    [
        # html.H2("Dash", className="display-3"),
        # html.Hr(),
        html.P(
            "Dash Apps", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("💸  Currency App", href="/apps/currency_app",
                            id="currency_app-link"),
                dbc.NavLink("Page 2", href="/apps/app1", id="page-1-link"),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


# content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
content = html.Div(id='page-content', style=CONTENT_STYLE)

# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    content
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/currency_app' or pathname == '/':
        return currency_app.layout
    elif pathname == '/apps/app1':
        return app1.layout
    else:
        return f'inconnu : {pathname}'


if __name__ == '__main__':
    app.run_server(debug=True)
