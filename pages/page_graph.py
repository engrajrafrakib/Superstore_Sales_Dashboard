# This page visualize a timeline graph and a bubble graph for the analysis of different useful properties.
# Import required modules
import pandas as pd
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from main import df_main

# Create a list of columns, those will be required for the table page.
column_list = ['Order Date', 'Ship Date', 'Customer Name', 'Region', 'State', 'City', 'Category', 'Sub-Category',
               'Product Name', 'Ship Mode', 'Sales', 'Profit', 'Profit Ratio', 'Discount', 'Quantity', 'Segment',
               'Days to Ship', 'Returned', 'Year', 'Month', 'Quarter', 'Week']
# Create page specific initial dataframe.
df = df_main[column_list]

# List of columns that are considered for the labeling to achieve bubble size parameter.
columns_to_label = ['Customer Name', 'Segment', 'Product Name', 'Ship Mode', 'Category', 'Sub-Category']
# Function to assign size/labels based on categorized properties. This size is required for the bubble graph.


def assign_integer_labels(df_resampled, column_names):
    labels_dict = {}
    for column_name in columns_to_label:
        # Assign integer labels to each unique value in the column.
        labels, levels = pd.factorize(df_resampled[column_name])
        # Create a dictionary to map values to integer labels.
        labels_dict[column_name] = labels
    # Create new columns with integer labels
    for column_name, labels in labels_dict.items():
        df_resampled[f'{column_name}_Label'] = labels
    return df_resampled


# Default dropdown options for Dropdown 1 and Dropdown 2.
fs_dropdown_options = [
    {'label': 'Days to Ship', 'value': 'Days to Ship'},
    {'label': 'Discount', 'value': 'Discount'},
    {'label': 'Profit', 'value': 'Profit'},
    {'label': 'Profit Ratio', 'value': 'Profit Ratio'},
    {'label': 'Quantity', 'value': 'Quantity'},
    {'label': 'Returns', 'value': 'Returned'},
    {'label': 'Sales', 'value': 'Sales'},
]
# Default dropdown options for Dropdown 3.
th_dropdown_options = [
    {'label': 'Segment', 'value': 'Segment_Label'},
    {'label': 'Ship Mode', 'value': 'Ship Mode_Label'},
    {'label': 'Customer Name', 'value': 'Customer Name_Label'},
    {'label': 'Category', 'value': 'Category_Label'},
    {'label': 'Sub-Category', 'value': 'Sub-Category_Label'},
    {'label': 'Product Name', 'value': 'Product Name_Label'}
]

# Design page header / title section.
page_header = dbc.CardGroup([
    dcc.Store(id='store-data', data=[], storage_type='memory'),
    dbc.Card(
        dbc.CardBody([
            html.H3("Graph Page", className="card-title", style={"font-size": 30}),
            html.P("Data visualization using timeline and bubble charts.", className="card-text")
            ])
        ),
    dbc.Card(
        html.Div(className="fa-solid fa-chart-simple",
                 style={"color": "white", "textAlign": "center", "fontSize": 24, "margin": "auto"}),
        className="bg-primary", style={"maxWidth": 75})], className="mt-4 shadow"
        )
# Design app layout for the graph page.
layout = html.Div([
    dbc.Row([
        dbc.Col(page_header, width=12),
    ], justify="center"),
    html.Br(),
    # Design date-filter and granularity dropdown section.
    dbc.Row([
       dbc.Col([
           dcc.DatePickerRange(
                id='date-range-picker',
                start_date=str(df['Order Date'].min()),
                end_date=str(df['Order Date'].max()),
                display_format='DD/MM/YYYY')
           ], width=5),
       # Granularity dropdown.
       dbc.Col([
           dcc.Dropdown(
                id='granularity-dropdown',
                options=[
                    {'label': 'Week', 'value': 'W'},
                    {'label': 'Month', 'value': 'ME'},
                    {'label': 'Quarter', 'value': 'QE'},
                    {'label': 'Year', 'value': 'YE'}
                    ],
                value='YE')
           ], width=7)
       ]),
    # Design graph section to create timeline and bubble chart with three dropdowns.
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='timeline-graph', figure=go.Figure()),
        ], width=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Label('Dropdown 1'),
                    dcc.Dropdown(
                        id='dropdown-1',
                        options=fs_dropdown_options
                        ),
                    html.Label('Dropdown 2'),
                    dcc.Dropdown(
                        id='dropdown-2',
                        options=fs_dropdown_options
                        ),
                    html.Label('Dropdown 3'),
                    dcc.Dropdown(
                        id='dropdown-3',
                        options=th_dropdown_options
                        )
                    ], width=3),
                dbc.Col([
                    dcc.Graph(id='bubble-graph')
                    ], width=9)
                ])
            ], width=7)
        ])
    ])

# Callback function to reorganize  Dropdown 2 options based on the Dropdown 1 selection.


@callback(
    Output('dropdown-2', 'options'),
    [Input('dropdown-1', 'value')]
)
def update_dropdown_2_options(selected_value):
    if selected_value:
        # Update initial dictionary list by excluding user selected option in dropdown 1. 
        updated_options = [option for option in fs_dropdown_options if option['value'] != selected_value]
        return updated_options
    else:
        return fs_dropdown_options
    
# Callback function to reorganize  Dropdown 1 options based on the Dropdown 2 selection.


@callback(
    Output('dropdown-1', 'options'),
    [Input('dropdown-2', 'value')]
)
def update_dropdown_1_options(selected_value):
    if selected_value:
        # Update initial dictionary list by excluding user selected option in dropdown 2. 
        updated_options = [option for option in fs_dropdown_options if option['value'] != selected_value]
        return updated_options
    else:
        return fs_dropdown_options
    
# Callback function to update the Buble graph.


@callback(
    Output('bubble-graph', 'figure'),
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date'),
     Input('granularity-dropdown', 'value'),
     Input('dropdown-1', 'value'),
     Input('dropdown-2', 'value'),
     Input('dropdown-3', 'value')]
)
def update_buble_graph(start_date, end_date, granularity, selected_value_1, selected_value_2, selected_value_3):
    df_date_filtered = df[df['Order Date'].between(start_date, end_date)]
    df_resampled = df_date_filtered.groupby(
        [pd.Grouper(key='Order Date', freq=granularity),
         'Region', 'Customer Name', 'Product Name',
         'Ship Mode', 'Segment', 'Category', 'Sub-Category'
         ]).agg({
            'Days to Ship': 'mean',
            'Sales': 'sum',
            'Profit': 'sum',
            'Discount': 'mean',
            'Quantity': 'sum',
            'Returned': 'sum',
            }).fillna(0)  # Fill NaN values with 0 for Week with no data.
    # Calculate Profit Ratio
    df_resampled['Profit Ratio'] = df_resampled['Profit'] / df_resampled['Sales']
    df_resampled = df_resampled.reset_index()
    df_resampled = assign_integer_labels(df_resampled, columns_to_label)
    
    # Validate user selections and update bubble graph accordingly.
    if (selected_value_1 or selected_value_2) and selected_value_3:
        df_resampled_2 = df_resampled.filter([selected_value_1, selected_value_2, selected_value_3], axis=1)
        fig = px.scatter(df_resampled_2, x=selected_value_1, y=selected_value_2, size=selected_value_3, size_max=20, title='Bubble Graph', color=df_resampled['Region'], hover_name=df_resampled[selected_value_3[:-6]], hover_data=[df_resampled["Order Date"], df_resampled["Product Name"]], labels={"color": "Region", selected_value_3: selected_value_3[:-6]+'Size', 'hover_data_0': 'Order Date', 'hover_data_1': 'Product Name'})
        return fig
    elif (selected_value_1 or selected_value_2) and selected_value_3 is None:
        df_resampled_2 = df_resampled.filter([selected_value_1, selected_value_2], axis=1)
        fig = px.scatter(df_resampled_2, x=selected_value_1, y=selected_value_2, title='Bubble Graph', color=df_resampled['Region'], labels={"color": "Region"})
        return fig

    elif (selected_value_1 is None and selected_value_2 is None):
        df_resampled_2 = df_resampled.filter([selected_value_1, selected_value_2], axis=1)
        fig = px.scatter(df_resampled_2, x=selected_value_1, y=selected_value_2, title='Bubble Graph')
        return fig
    else:
        raise PreventUpdate

# Callback function to update Timeline graph.    


@callback(
    Output('timeline-graph', 'figure'),
    [Input('granularity-dropdown', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_timeline_graph(granularity, start_date, end_date):
    # Reducing dataframe size by considering only relevant fields.
    list_columns = ['Order Date', 'Days to Ship', 'Returned', 'Sales', 'Profit']
    df_filtered = df[list_columns]
    # Filter data based on the date filter.
    df_date_filtered = df_filtered[df_filtered['Order Date'].between(start_date, end_date)]
    
    # Resample data based on selected granularity.
    df_resampled = df_date_filtered.groupby([pd.Grouper(key='Order Date', freq=granularity)]).agg({
        'Days to Ship': 'mean',
        'Sales': 'sum',
        'Profit': 'sum',
        'Returned': 'sum'
        }).fillna(0).reset_index()  # Fill NaN values with 0
    # Reformat dates for better visualization and readability in the timeline graph.
    if granularity == 'W':
        df_resampled['Order Date'] = df_resampled['Order Date'].dt.year.astype(str) + 'CW' + df_resampled['Order Date'].dt.isocalendar().week.astype(str) 
    elif granularity == 'ME':
        df_resampled['Order Date'] = df_resampled['Order Date'].dt.year.astype(str) + 'M' + df_resampled['Order Date'].dt.month.astype(str) 
    elif granularity == 'QE':
        df_resampled['Order Date'] = df_resampled['Order Date'].dt.year.astype(str) + 'Q' + df_resampled['Order Date'].dt.quarter.astype(str) 
    elif granularity == 'YE':
        df_resampled['Order Date'] = df_resampled['Order Date'].dt.year.astype(str) 
    else:
        df_resampled = df_date_filtered
        
    # Calculate Profit Ratio
    df_resampled['Profit Ratio'] = round(df_resampled['Profit']*100 / df_resampled['Sales'], 2)
    # Update Timeline graph.
    fig = go.Figure(
        px.line(df_resampled, 
                x='Order Date', 
                y=['Days to Ship', 'Sales', 'Profit', 'Profit Ratio', 'Returned'], 
                title='Timeline Graph',
                labels={"value": "Value", "Order Date": "Time Period", "variable": "Properties"}, 
                markers=True,
                log_y=True))
    fig.update_layout(template='plotly_white')
    fig.update_xaxes(tickformat='%Y-%m-%d', mirror=True, ticks='outside', showline=False, linecolor='white', gridcolor='white')
    fig.update_yaxes(ticks='outside', showline=False, linecolor='white', gridcolor='white')
    return fig
