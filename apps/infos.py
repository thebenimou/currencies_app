from tools import human_format
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app

from .components import ModernCard


layout = html.Div(
    [
        ModernCard(
            children=[dbc.CardBody("This is some text within a card body !")],
        ),
    ]
)
