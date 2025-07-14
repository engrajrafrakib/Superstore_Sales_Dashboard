# This page visualizes the datatable with filtering and record insertion features
# Import required modules
from dash import dash_table, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from main import df_main

# Color scheme
COLOR_PRIMARY = '#2E86AB'
COLOR_SECONDARY = '#F18F01'
COLOR_SUCCESS = '#3D9970'
COLOR_DANGER = '#FF4136'
COLOR_LIGHT = '#F5F5F5'
COLOR_DARK = '#333333'

# Card styling
CARD_STYLE = {
    'borderRadius': '10px',
    'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
    'marginBottom': '20px',
    'backgroundColor': 'white'
}

# Create a list of columns required for the table page
column_list = ['Region', 'State', 'City', 'Order Date', 'Ship Date', 'Category', 'Sub-Category',
               'Sales', 'Profit', 'Profit Ratio', 'Discount', 'Quantity', 'Segment', 'Days to Ship', 'Returned']
# Create page specific initial dataframe
df = df_main[column_list]
# Create a list of updatable columns
input_fields = ['Region', 'State', 'City', 'Category', 'Sub-Category']

# Design page header / title section
page_header = dbc.Card(
    dbc.CardBody([
        html.H2("Sales Data Explorer", className="card-title", style={'color': COLOR_DARK}),
        html.P("Interactive table with filtering and data entry capabilities",
               className="card-text", style={'color': COLOR_DARK}),
        html.Hr(style={'borderTop': f'2px solid {COLOR_PRIMARY}'})
    ]),
    style={
        **CARD_STYLE,
        'borderLeft': f'5px solid {COLOR_PRIMARY}',
        'marginTop': '20px'
    }
)

# Design app layout for the datatable page
layout = html.Div([
    # Pop up messages
    dcc.ConfirmDialog(
        id='no-update',
        displayed=False,
        message='Region already exists!',
        submit_n_clicks=0
    ),
    dcc.ConfirmDialog(
        id='data-update',
        displayed=False,
        message='Record successfully added!',
        submit_n_clicks=0
    ),

    # Page header
    dbc.Row(dbc.Col(page_header, width=12)),

    # Filters section
    dbc.Card(
        dbc.CardBody([
            html.H5("Data Filters", className="card-title",
                    style={'color': COLOR_PRIMARY, 'marginBottom': '15px'}),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Rows per page:", className="mb-1"),
                    dcc.Dropdown(
                        id='row-dropdown',
                        value=25,
                        clearable=False,
                        options=[10, 25, 50, 100],
                        style={'width': '100%'}
                    )
                ], width=2),

                dbc.Col([
                    dbc.Label("Region:", className="mb-1"),
                    dcc.Dropdown(
                        id='region',
                        options=[{'label': x, 'value': x} for x in sorted(df['Region'].unique())],
                        multi=False,
                        placeholder="Select region...",
                        style={'width': '100%'}
                    )
                ], width=3),

                dbc.Col([
                    dbc.Label("State:", className="mb-1"),
                    dcc.Dropdown(
                        id='state',
                        options=[{'label': x, 'value': x} for x in sorted(df['State'].unique())],
                        multi=False,
                        placeholder="Select state...",
                        style={'width': '100%'}
                    )
                ], width=3),

                dbc.Col([
                    dbc.Label("City:", className="mb-1"),
                    dcc.Dropdown(
                        id='city',
                        options=[{'label': x, 'value': x} for x in sorted(df['City'].unique())],
                        multi=False,
                        placeholder="Select city...",
                        style={'width': '100%'}
                    )
                ], width=3)
            ], className='mb-3')
        ]),
        style=CARD_STYLE
    ),

    # Data table section
    dbc.Card(
        dbc.CardBody([
            html.H5("Sales Records", className="card-title",
                    style={'color': COLOR_PRIMARY, 'marginBottom': '15px'}),

            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                style_table={
                    'overflowX': 'auto',
                    'height': '600px',
                    'borderRadius': '8px'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontFamily': 'Arial, sans-serif',
                    'border': '1px solid #e0e0e0'
                },
                style_header={
                    'backgroundColor': COLOR_PRIMARY,
                    'color': 'white',
                    'fontWeight': 'bold',
                    'border': '1px solid #e0e0e0'
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'border': '1px solid #e0e0e0'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgba(240, 240, 240, 0.5)'
                    }
                ],
                filter_action="native",
                sort_action="native",
                row_deletable=True,
                editable=True,
                page_action="native",
                page_current=0,
                page_size=25,
                fixed_rows={'headers': True}
            )
        ]),
        style=CARD_STYLE
    ),

    # Add new record section
    dbc.Card(
        dbc.CardBody([
            html.H5("Add New Record", className="card-title",
                    style={'color': COLOR_PRIMARY, 'marginBottom': '15px'}),

            dbc.Row([
                dbc.Col([
                    dbc.Input(
                        id=f'input_{field}',
                        placeholder=f"Enter {field}...",
                        className="mb-2",
                        style={'width': '100%'}
                    )
                ], width=2) for field in input_fields
            ], className='mb-3'),

            dbc.Row(
                dbc.Col(
                    dbc.Button(
                        'Add New Record',
                        id='submit-button',
                        n_clicks=0,
                        color="primary",
                        className="me-1",
                        style={'width': '200px'}
                    ),
                    width=12, className="text-center"
                )
            )
        ]),
        style=CARD_STYLE
    )
], style={
    'backgroundColor': COLOR_LIGHT,
    'padding': '20px'
})


# Callback function to handle user dropdown selections
@callback(
    Output('data-table', 'data'),
    Output('data-table', 'page_size'),
    Output('region', 'options'),
    Output('state', 'options'),
    Output('city', 'options'),
    Input('region', 'value'),
    Input('state', 'value'),
    Input('city', 'value'),
    Input('row-dropdown', 'value')
)
def update_dropdown_options(region_v, state_v, city_v, row_v):
    df_filtered = df.copy()
    if region_v:
        df_filtered = df_filtered[df_filtered.Region == region_v].sort_values(column_list)
    if state_v:
        df_filtered = df_filtered[df_filtered.State == state_v]
    if city_v:
        df_filtered = df_filtered[df_filtered.City == city_v]

    return (
        df_filtered.to_dict('records'),
        row_v,
        [{'label': i, 'value': i} for i in sorted(df_filtered['Region'].unique())],
        [{'label': i, 'value': i} for i in sorted(df_filtered['State'].unique())],
        [{'label': i, 'value': i} for i in sorted(df_filtered['City'].unique())]
    )


# Callback function to perform datatable update based on user new row entries
@callback(
    [Output('no-update', 'displayed'),
     Output('data-update', 'displayed'),
     Output('data-table', 'data', allow_duplicate=True)],
    Input('submit-button', 'n_clicks'),
    [State('data-table', 'columns')],
    [State(f'input_{x}', 'value') for x in input_fields],
    prevent_initial_call=True
)
def update_datatable(n_clicks, columns, input_region, input_state, input_city, input_category, input_subcategory):
    if n_clicks > 0:
        if input_region in df['Region'].values:
            data_updated = df.to_dict('records')
            return True, False, data_updated
        else:
            new_row = {c['id']: r for c, r in zip(columns, [
                input_region, input_state, input_city, None, None,  # Order Date and Ship Date set to None
                input_category, input_subcategory, None, None, None,  # Sales, Profit, Profit Ratio set to None
                None, None, None, None, None  # Discount, Quantity, Segment, Days to Ship, Returned set to None
            ])}

            if any(x is None for x in [input_region, input_state, input_city, input_category, input_subcategory]):
                raise PreventUpdate
            else:
                df.loc[len(df)] = new_row
                data_updated = df.to_dict('records')
                return False, True, data_updated
    else:
        raise PreventUpdate