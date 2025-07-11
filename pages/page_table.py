# This page visualize the datatable with some feature for filtering and insertion of new records.
# Import required modules
from dash import dash_table, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from main import *

# Create a list of columns, those are required for the table page.
column_list = ['Region','State','City','Order Date','Ship Date','Category','Sub-Category','Sales','Profit', 'Profit Ratio','Discount','Quantity','Segment','Days to Ship','Returned']
# Create page specific initial dataframe.
df = df_main[column_list]
# Create a list of updatable columns.
input_fields = ['Region', 'State', 'City', 'Category', 'Sub-Category']

# Design page header / title section.
page_header = dbc.CardGroup([
    dbc.Card(
        dbc.CardBody(
            [
                html.H3("Sales Data Table", className="card-title", style={"font-size":30}),
                html.P("Mostly utilized data are displayed in this datatable.", className="card-text"),
            ])
        ),
    dbc.Card(
        html.Div(className="fa-solid fa-database", style={"color": "white","textAlign": "center","fontSize": 24,"margin": "auto"}),
        className="bg-primary",
        style={"maxWidth": 75}
        )], className="mt-4 shadow"
    )

# Design app layout for the datatable page.
layout = html.Div([
    # Pop up message for input fields insertion validation.
    dcc.ConfirmDialog(
        id='no-update',
        displayed=False,
        message='Region already exists!'
        ),
    # Pop up message for input fields insertion validation.
    dcc.ConfirmDialog(
        id='data-update',
        displayed=False,
        message='Region Successfully Updated!',
        ),
    dbc.Row([
        dbc.Col(page_header, width=12)
        ], justify="center"),
    html.Br(),
    dbc.Label("Show number of rows"),
    html.Br(),
    # Design dropdowns to filter datatable.
    row_dropdown := dcc.Dropdown(value=25, clearable=False, style={'width':'35%', 'align':'right'}, options=[10, 25, 50, 100]),
    dbc.Row([
        dbc.Col([region_dropdown := dcc.Dropdown(id = 'region', options=[x for x in sorted(df['Region'].unique())], multi=False)
            ], width=4),
        dbc.Col([
            state_dropdown := dcc.Dropdown(id = 'state', options=[x for x in sorted(df['State'].unique())], multi=False)
            ], width=4),
        dbc.Col([
            city_dropdown := dcc.Dropdown(id = 'city', options=[x for x in sorted(df['City'].unique())], multi=False)
            ], width=4)
        ], justify="between", className='mt-3 mb-4'),
    # Design Datatable
    dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                style_table={'overflow': 'scroll', 'height': 800},
                style_cell={'textAlign': 'center'},
                row_deletable=True,
                editable=True,
                style_header={'backgroundColor': '#35384b', 'color': 'white', 'fontWeight': 'bold'},
                style_data={'width': '150px', 'minWidth': '150px', 'maxWidth': '150px', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(220, 220, 220)'}]),
    # Input fields to add new rows into the datatable.
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Input(
                    id='input_{}'.format(x),
                    placeholder="Insert {}".format(x),  
                    minLength=0, maxLength=50,          
                    autoComplete='on',
                    disabled=False,                    
                    readOnly=False,                     
                    required=False,                    
                    size="30"
                    )], width=2) for x in input_fields
            ], justify="center", className='mt-3 mb-4')
        ]),
    # Button to add new entries into the datatable.
    dbc.Row([
        html.Button('Add Row', id='submit-button', n_clicks=0, style={'background-color': '#35384b', 'color':'white'})
    ], className="button")
])
# Callback function to handle user dropdown selections.
@callback(
    Output('data-table', 'data'),
    Output('data-table', 'page_size'),
    Output('region', 'options'),
    Output('state', 'options'),
    Output('city', 'options'),
    [Input(region_dropdown, 'value'),
    Input(state_dropdown, 'value'),
    Input(city_dropdown, 'value'),],
    Input(row_dropdown, 'value')
    )

def update_dropdown_options(region_v,state_v, city_v, row_v):
    # Make a copy of original dataframe to ensure that modifications are made only on copied dataframe. 
    df_filtered = df.copy()
    if region_v:
        df_filtered = df_filtered[df_filtered.Region == region_v].sort_values(column_list)
    if state_v:
        df_filtered = df_filtered[df_filtered.State == state_v]
    if city_v:
        df_filtered = df_filtered[df_filtered.City == city_v]
    return df_filtered.to_dict('records'), row_v, [{'label': i, 'value': i} for i in sorted(df_filtered['Region'].unique())], [{'label': i, 'value': i} for i in sorted(df_filtered['State'].unique())], [{'label': i, 'value': i} for i in sorted(df_filtered['City'].unique())]

# Callback function to perform datatable update based on user new row entries.
@callback([Output('no-update', 'displayed'), Output('data-update', 'displayed'), Output('data-table', 'data', allow_duplicate=True)],
              [Input('submit-button', 'n_clicks')],
              [State('data-table', 'columns')], 
              [State('input_{}'.format(x), 'value') for x in input_fields], prevent_initial_call=True)

def update_datatable(n_clicks, columns, input_region, input_state, input_city, input_category, input_subcategory):
    if n_clicks > 0:
        if input_region in df['Region'].values:
            data_updated = df.to_dict('records')
            return True, False, data_updated
        else:
            new_row = {c['id']: r for c, r in zip(columns, [input_region, input_state, input_city,
                input_category, input_subcategory])}
            if any(x is None for x in new_row.values()):
                raise PreventUpdate
            else:
                df.loc[len(df)] = new_row
                data_updated = df.to_dict('records')
                return False, True, data_updated
    else:
        return False, False, data_updated