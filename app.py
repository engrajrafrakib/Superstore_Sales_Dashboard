# Import required modules
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from main import *

# Connect to app pages
from pages import page_landing, page_table, page_graph

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUMEN, font_awesome])

# create app layout
app.layout = html.Div([ 
    dcc.Location(id='url', refresh=True),
    dbc.Row([
    dbc.Col([
        html.Div([
            html.Div([
                html.H5("Dashboard", style={'color': 'White', 'margin-top': '10px'}),
                html.Img(src="/assets/icon_dashboard.png"),
                ], className='image-title'),
            html.Hr(),
            dbc.Nav([
                dbc.NavLink([
                    html.I(className="fa-solid fa-house-user"),
                    html.Span("Overview", style={'margin-top': '3px'})], className='icon-title',
                    href="/",
                    active="exact"
                    ),
                dbc.NavLink([
                    html.I(className="fa-solid fa-database"),
                    html.Span("DataTable", style={'margin-top': '3px'})], className='icon-title',
                    href="/pages/table",
                    active="exact"
                    ),
                dbc.NavLink([
                    html.I(className="fa-solid fa-chart-simple"),
                    html.Span("Graph", style={'margin-top': '3px'})], className='icon-title',
                    href="/pages/graph",
                    active="exact"
                    )], pills=True
                    )
            ], className="sidebar"
                 )
        ], width=1),
    dbc.Col([
        html.Div(id='page-content', children=[])
        ], width=11),
    ])
    ])

# Callback function to communicate with all pages
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return page_landing.layout
    elif pathname == '/pages/table':
        return page_table.layout
    elif pathname == '/pages/graph':
        return page_graph.layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)

