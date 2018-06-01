import dash_core_components as dcc
import dash_html_components as html
from ourpackage import app

layout = app.layout = html.Div(children=[
    html.H1("Hey, this is my first dash app!"),
    html.P("Still under construction... :)"),
    dcc.Graph(
        id = "uber_pricing_graph",
        figure = {
            'data': [
                {'name': "Brooklyn",
                'x': [0.86, 1.5, 2.2, 2.6, 2.7, 3, 3.67],
                'y': [6.40, 8.34, 9.46, 11.13, 12.55, 18.68],
                'type': "line"},
                {'name': "Manhattan",
                'x': [0.93, 1.33, 2.6, 2.4, 2.94, 3.34, 4.11],
                'y': [9.34, 10.09, 13.24, 16.53, 15.64, 25.65],
                'type': "line"}
            ],
            'layout': {
                'title': 'Uber Pricing in Brooklyn and Manhattan'
            }
        }
    )
])
