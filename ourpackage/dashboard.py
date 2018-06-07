import dash_core_components as dcc
import dash_html_components as html
from ourpackage import app
from ourpackage.uber_data import data

app.layout = html.Div(children=[
    html.H1("Check it out! This app has Flask AND Dash!"),
    html.P("Adding some cool graph here soon:"),
    dcc.Graph(
        id = "uber_pricing_graph",
        figure = {
            'data': data,
            'layout': {
                'title': 'Uber Pricing in Brooklyn and Manhattan'
            }
        }
    )
])
