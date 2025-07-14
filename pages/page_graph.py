# This page visualizes a timeline graph and a bubble graph for data analysis
# Import required modules
import pandas as pd
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
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

# Create a list of columns required for the page
column_list = ['Order Date', 'Ship Date', 'Customer Name', 'Region', 'State', 'City', 'Category', 'Sub-Category',
               'Product Name', 'Ship Mode', 'Sales', 'Profit', 'Profit Ratio', 'Discount', 'Quantity', 'Segment',
               'Days to Ship', 'Returned', 'Year', 'Month', 'Quarter', 'Week']
df = df_main[column_list]

# List of columns for bubble size parameter
columns_to_label = ['Customer Name', 'Segment', 'Product Name', 'Ship Mode', 'Category', 'Sub-Category']


def assign_integer_labels(df_resampled, column_names):
    labels_dict = {}
    for column_name in columns_to_label:
        labels, levels = pd.factorize(df_resampled[column_name])
        labels_dict[column_name] = labels
    for column_name, labels in labels_dict.items():
        df_resampled[f'{column_name}_Label'] = labels
    return df_resampled


# Dropdown options
fs_dropdown_options = [
    {'label': 'Days to Ship', 'value': 'Days to Ship'},
    {'label': 'Discount', 'value': 'Discount'},
    {'label': 'Profit', 'value': 'Profit'},
    {'label': 'Profit Ratio', 'value': 'Profit Ratio'},
    {'label': 'Quantity', 'value': 'Quantity'},
    {'label': 'Returns', 'value': 'Returned'},
    {'label': 'Sales', 'value': 'Sales'},
]

th_dropdown_options = [
    {'label': 'Segment', 'value': 'Segment_Label'},
    {'label': 'Ship Mode', 'value': 'Ship Mode_Label'},
    {'label': 'Customer Name', 'value': 'Customer Name_Label'},
    {'label': 'Category', 'value': 'Category_Label'},
    {'label': 'Sub-Category', 'value': 'Sub-Category_Label'},
    {'label': 'Product Name', 'value': 'Product Name_Label'}
]

# Page header
page_header = dbc.Card(
    dbc.CardBody([
        html.H2("Sales Analytics Dashboard", className="card-title", style={'color': COLOR_DARK}),
        html.P("Interactive visualization of sales data with timeline and bubble charts",
               className="card-text", style={'color': COLOR_DARK}),
        html.Hr(style={'borderTop': f'2px solid {COLOR_PRIMARY}'})
    ]),
    style={
        **CARD_STYLE,
        'borderLeft': f'5px solid {COLOR_PRIMARY}',
        'marginTop': '20px'
    }
)

# Layout
layout = html.Div([
    # Store component
    dcc.Store(id='store-data', data=[], storage_type='memory'),

    # Header
    dbc.Row(dbc.Col(page_header, width=12)),

    # Filters section
    dbc.Card(
        dbc.CardBody([
            html.H5("Data Filters", className="card-title",
                    style={'color': COLOR_PRIMARY, 'marginBottom': '15px'}),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Date Range:", className="mb-1"),
                    dcc.DatePickerRange(
                        id='date-range-picker',
                        start_date=str(df['Order Date'].min()),
                        end_date=str(df['Order Date'].max()),
                        display_format='DD/MM/YYYY',
                        style={'width': '100%'}
                    )
                ], width=6),

                dbc.Col([
                    dbc.Label("Time Granularity:", className="mb-1"),
                    dcc.Dropdown(
                        id='granularity-dropdown',
                        options=[
                            {'label': 'Weekly', 'value': 'W'},
                            {'label': 'Monthly', 'value': 'ME'},
                            {'label': 'Quarterly', 'value': 'QE'},
                            {'label': 'Yearly', 'value': 'YE'}
                        ],
                        value='YE',
                        clearable=False,
                        style={'width': '100%'}
                    )
                ], width=6)
            ])
        ]),
        style=CARD_STYLE
    ),

    # Visualization section
    dbc.Row([
        # Timeline graph
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Sales Timeline", className="card-title",
                            style={'color': COLOR_PRIMARY, 'marginBottom': '15px'}),
                    dcc.Graph(
                        id='timeline-graph',
                        figure=go.Figure(),
                        style={'height': '500px'}
                    )
                ]),
                style=CARD_STYLE
            ),
            width=12, lg=6, className="mb-4"
        ),

        # Bubble graph with controls
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Bubble Chart Analysis", className="card-title",
                            style={'color': COLOR_PRIMARY, 'marginBottom': '15px'}),

                    dbc.Row([
                        dbc.Col([
                            dbc.Label("X-Axis:", className="mb-1"),
                            dcc.Dropdown(
                                id='dropdown-1',
                                options=fs_dropdown_options,
                                placeholder="Select X-axis...",
                                style={'width': '100%'}
                            ),

                            dbc.Label("Y-Axis:", className="mb-1 mt-3"),
                            dcc.Dropdown(
                                id='dropdown-2',
                                options=fs_dropdown_options,
                                placeholder="Select Y-axis...",
                                style={'width': '100%'}
                            ),

                            dbc.Label("Bubble Size:", className="mb-1 mt-3"),
                            dcc.Dropdown(
                                id='dropdown-3',
                                options=th_dropdown_options,
                                placeholder="Select size...",
                                style={'width': '100%'}
                            )
                        ], width=4),

                        dbc.Col([
                            dcc.Graph(
                                id='bubble-graph',
                                style={'height': '450px'}
                            )
                        ], width=8)
                    ])
                ]),
                style=CARD_STYLE
            ),
            width=12, lg=6, className="mb-4"
        )
    ])
], style={
    'backgroundColor': COLOR_LIGHT,
    'padding': '20px'
})


# Callbacks remain the same as in your original code
@callback(
    Output('dropdown-2', 'options'),
    [Input('dropdown-1', 'value')]
)
def update_dropdown_2_options(selected_value):
    if selected_value:
        updated_options = [option for option in fs_dropdown_options if option['value'] != selected_value]
        return updated_options
    return fs_dropdown_options


@callback(
    Output('dropdown-1', 'options'),
    [Input('dropdown-2', 'value')]
)
def update_dropdown_1_options(selected_value):
    if selected_value:
        updated_options = [option for option in fs_dropdown_options if option['value'] != selected_value]
        return updated_options
    return fs_dropdown_options


@callback(
    Output('bubble-graph', 'figure'),
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date'),
     Input('granularity-dropdown', 'value'),
     Input('dropdown-1', 'value'),
     Input('dropdown-2', 'value'),
     Input('dropdown-3', 'value')]
)
def update_bubble_graph(start_date, end_date, granularity, selected_value_1, selected_value_2, selected_value_3):
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
    }).fillna(0)

    df_resampled['Profit Ratio'] = df_resampled['Profit'] / df_resampled['Sales']
    df_resampled = df_resampled.reset_index()
    df_resampled = assign_integer_labels(df_resampled, columns_to_label)

    if (selected_value_1 or selected_value_2) and selected_value_3:
        fig = px.scatter(
            df_resampled,
            x=selected_value_1,
            y=selected_value_2,
            size=selected_value_3,
            size_max=20,
            color='Region',
            hover_name=selected_value_3[:-6],
            hover_data=["Order Date", "Product Name"],
            title='',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
    elif (selected_value_1 or selected_value_2) and selected_value_3 is None:
        fig = px.scatter(
            df_resampled,
            x=selected_value_1,
            y=selected_value_2,
            color='Region',
            title='',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
    else:
        raise PreventUpdate


@callback(
    Output('timeline-graph', 'figure'),
    [Input('granularity-dropdown', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_timeline_graph(granularity, start_date, end_date):
    list_columns = ['Order Date', 'Days to Ship', 'Returned', 'Sales', 'Profit']
    df_filtered = df[list_columns]
    df_date_filtered = df_filtered[df_filtered['Order Date'].between(start_date, end_date)]

    df_resampled = df_date_filtered.groupby([pd.Grouper(key='Order Date', freq=granularity)]).agg({
        'Days to Ship': 'mean',
        'Sales': 'sum',
        'Profit': 'sum',
        'Returned': 'sum'
    }).fillna(0).reset_index()

    if granularity == 'W':
        df_resampled['Order Date'] = df_resampled['Order Date'].dt.year.astype(str) + ' CW' + df_resampled[
            'Order Date'].dt.isocalendar().week.astype(str)
    elif granularity == 'ME':
        df_resampled['Order Date'] = df_resampled['Order Date'].dt.year.astype(str) + ' M' + df_resampled[
            'Order Date'].dt.month.astype(str)
    elif granularity == 'QE':
        df_resampled['Order Date'] = df_resampled['Order Date'].dt.year.astype(str) + ' Q' + df_resampled[
            'Order Date'].dt.quarter.astype(str)
    elif granularity == 'YE':
        df_resampled['Order Date'] = df_resampled['Order Date'].dt.year.astype(str)
    else:
        df_resampled = df_date_filtered

    df_resampled['Profit Ratio'] = round(df_resampled['Profit'] * 100 / df_resampled['Sales'], 2)

    fig = go.Figure()
    for col in ['Days to Ship', 'Sales', 'Profit', 'Profit Ratio', 'Returned']:
        fig.add_trace(go.Scatter(
            x=df_resampled['Order Date'],
            y=df_resampled[col],
            name=col,
            mode='lines+markers',
            hovertemplate='%{x}<br>%{y:.2f}<extra></extra>'
        ))

    fig.update_layout(
        title='',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode="x unified"
    )

    return fig