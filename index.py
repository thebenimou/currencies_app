import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import currency_app, app1, infos

server = app.server

pages = {
    "/apps/currency_app": {
        "title": "💸  Currencies",
        "id": "currency_app-link",
        "app": currency_app.layout
    },
    "/apps/app1": {
        "title": "🏪 Superstore",
        "id": "page-1-link",
        "app": app1.layout
    },
    "/apps/infos": {
        "title": "ℹ Infos",
        "id": "page-2-link",
        "app": infos.layout
    }
}


# menu - faire un fichier à part
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
            [dbc.NavLink(m[1]['title'], href=m[0], id=m[1]['id'])
             for m in pages.items()],
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
    if pathname in pages.keys():
        return pages[pathname]["app"]
    if pathname == "/":
        return pages["/apps/currency_app"]['app']
    else:
        # faire un template joli de page
        return f"Cette page n'existe pas : {pathname}"


@app.callback(
    [Output(f"{m[1]['id']}", "active") for m in pages.items()],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # ici on avoir len(pages.items()) elements, à automatiser
        # return True, False
        return [True] + [False for m in range(len(pages.keys())-1)]
    return [pathname == f"{m[0]}" for m in pages.items()]


if __name__ == '__main__':
    app.run_server(debug=True)
