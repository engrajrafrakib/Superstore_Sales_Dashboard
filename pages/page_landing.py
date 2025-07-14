# This page gives the general overview of different properties to analyze the sales data.
# Import required modules
import pandas as pd
from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from main import df_main

# Common styling constants
COLOR_PRIMARY = '#2E86AB'
COLOR_SECONDARY = '#F18F01'
COLOR_SUCCESS = '#3D9970'
COLOR_DANGER = '#FF4136'
COLOR_LIGHT = '#F5F5F5'
COLOR_DARK = '#333333'

CARD_STYLE = {
    'borderRadius': '10px',
    'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
    'marginBottom': '20px',
    'backgroundColor': 'white'
}

CARD_HEADER_STYLE = {
    'backgroundColor': COLOR_PRIMARY,
    'color': 'white',
    'borderRadius': '10px 10px 0 0',
    'padding': '15px'
}

CARD_BODY_STYLE = {
    'padding': '20px'
}

GRAPH_STYLE = {
    'height': '100%',
    'width': '100%'
}

# Create a list of columns, those are required for the landing page.
column_list = ['Order Date', 'Sales', 'Profit', 'Days to Ship', 'Region', 'Category', 'Segment']
# Create page specific initial dataframe.
df = df_main[column_list]

# Designing page layout by initializing different blocks/sections.
# Design the page header/title block.
page_header = dbc.Card(
    dbc.CardBody([
        html.H2("Sales Dashboard", className="card-title", style={'color': COLOR_DARK}),
        html.P("General overview of the Sales Data", className="card-text", style={'color': COLOR_DARK}),
        html.Hr(style={'borderTop': f'2px solid {COLOR_PRIMARY}'})
    ],
        style={
            **CARD_STYLE,
            'borderLeft': f'5px solid {COLOR_PRIMARY}',
            'marginTop': '20px'
        }
    ))

# Design the date-filter block.
selection_filter = dbc.Card(
    dbc.CardBody([
        html.H5("Select Date Range", className="card-title", style={'color': COLOR_DARK}),
        dcc.DatePickerRange(
            id='date-range-picker',
            start_date='2017-01-01',
            end_date='2017-12-31',
            display_format='DD/MM/YYYY',
            style={'width': '100%'},
            className='mb-3'
        )
    ]),
    style=CARD_STYLE
)

# Helper function to create metric cards


def create_metric_card(title, figure_id, color):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title", style={'textAlign': 'center'}),
            dcc.Graph(
                id=figure_id,
                figure=go.Figure(),
                style=GRAPH_STYLE,
                config={'displayModeBar': False}
            )
        ]),
        style={
            **CARD_STYLE,
            'borderTop': f'5px solid {color}'
        }
    )


# Create metric cards
overview_chart_1 = create_metric_card("Total Sales", 'overview-sales', COLOR_PRIMARY)
overview_chart_2 = create_metric_card("Total Profit", 'overview-profit', COLOR_SECONDARY)
overview_chart_3 = create_metric_card("Profit Ratio", 'overview-profit-ratio', COLOR_SUCCESS)
overview_chart_4 = create_metric_card("Avg Days to Ship", 'overview-average-days-to-ship', COLOR_DANGER)


# Helper function to create breakdown cards
def create_breakdown_card(title, figure_id, color):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title", style={'textAlign': 'center'}),
            dcc.Graph(
                id=figure_id,
                figure=go.Figure(),
                style=GRAPH_STYLE
            )
        ]),
        style={
            **CARD_STYLE,
            'borderTop': f'5px solid {color}'
        }
    )


# Create breakdown cards
overview_chart_5 = create_breakdown_card("Sales by Region", 'overview-sales-by-region', COLOR_PRIMARY)
overview_chart_6 = create_breakdown_card("Profit by Region", 'overview-profit-by-region', COLOR_SECONDARY)
overview_chart_7 = create_breakdown_card("Profit Ratio by Region", 'overview-profit-ratio-by-region', COLOR_SUCCESS)
overview_chart_8 = create_breakdown_card("Avg Days to Ship by Region", 'overview-average-days-to-ship-by-region',
                                         COLOR_DANGER)


# Helper function to create pie chart cards
def create_pie_card(title, figure_id, color, link_text, link_href):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title", style={'textAlign': 'center'}),
            dcc.Graph(
                id=figure_id,
                figure=go.Figure(),
                style=GRAPH_STYLE
            ),
            dbc.Button(
                link_text,
                href=link_href,
                color="primary",
                className="mt-2",
                style={'width': '100%'}
            )
        ]),
        style={
            **CARD_STYLE,
            'borderTop': f'5px solid {color}'
        }
    )


# Create pie chart cards
overview_chart_9 = create_pie_card(
    "Sales by Category",
    'overview-sales-by-category',
    COLOR_PRIMARY,
    "View DataTable",
    "/pages/table"
)

overview_chart_10 = create_pie_card(
    "Sales by Segment",
    'overview-sales-by-segment',
    COLOR_SECONDARY,
    "View Graphs",
    "/pages/graph"
)

# Structuring the main layout of the page.
layout = html.Div([
    # Page title/header
    dbc.Row(
        dbc.Col(page_header, width=12),
        className="mb-4"
    ),

    # Date filter
    dbc.Row(
        dbc.Col(selection_filter, width=12, lg=8, className="mx-auto"),
        className="mb-4"
    ),

    # First row of metric cards
    dbc.Row([
        dbc.Col(overview_chart_1, xs=12, sm=6, md=3, className="mb-4"),
        dbc.Col(overview_chart_2, xs=12, sm=6, md=3, className="mb-4"),
        dbc.Col(overview_chart_3, xs=12, sm=6, md=3, className="mb-4"),
        dbc.Col(overview_chart_4, xs=12, sm=6, md=3, className="mb-4"),
    ], className="mb-4"),

    # Second row of breakdown cards
    dbc.Row([
        dbc.Col(overview_chart_5, xs=12, sm=6, md=3, className="mb-4"),
        dbc.Col(overview_chart_6, xs=12, sm=6, md=3, className="mb-4"),
        dbc.Col(overview_chart_7, xs=12, sm=6, md=3, className="mb-4"),
        dbc.Col(overview_chart_8, xs=12, sm=6, md=3, className="mb-4"),
    ], className="mb-4"),

    # Third row of pie charts
    dbc.Row([
        dbc.Col(overview_chart_9, xs=12, md=6, className="mb-4"),
        dbc.Col(overview_chart_10, xs=12, md=6, className="mb-4"),
    ])
], style={
    'backgroundColor': COLOR_LIGHT,
    'minHeight': '100vh',
    'padding': '20px'
})


# Create additional dataframes by aggregating relevant information.
def filter_and_aggregate(df, column, start_date, end_date):
    df_filtered = df[df['Order Date'].between(start_date, end_date)]
    df_filtered = df_filtered.groupby(column).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Days to Ship': 'mean'
    }).reset_index()
    return df_filtered


# Callback function to update overview charts
@callback([
    Output('overview-sales', 'figure'),
    Output('overview-profit', 'figure'),
    Output('overview-profit-ratio', 'figure'),
    Output('overview-average-days-to-ship', 'figure'),
    Output('overview-sales-by-region', 'figure'),
    Output('overview-profit-by-region', 'figure'),
    Output('overview-profit-ratio-by-region', 'figure'),
    Output('overview-average-days-to-ship-by-region', 'figure'),
    Output('overview-sales-by-category', 'figure'),
    Output('overview-sales-by-segment', 'figure')],
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')])
def update_overview_cards(start_date, end_date):
    if start_date and end_date:
        df_filtered = df[df['Order Date'].between(start_date, end_date)]
        # Group by 'Order Date' and calculate the aggregated values.
        df_filtered = df_filtered.groupby('Order Date').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Days to Ship': 'mean'
        }).reset_index()
        # Calculate Profit Ratio.
        df_filtered['Profit Ratio'] = df_filtered['Profit'] / df_filtered['Sales']

        # Use Pandas shift method to estimate prior periods sales information.
        df_filtered['PP_Sales'] = df_filtered['Sales'].shift(1).fillna(0)
        df_filtered['PP_Profit'] = df_filtered['Profit'].shift(1).fillna(0)
        df_filtered['PP_Days_to_Ship'] = df_filtered['Days to Ship'].shift(1).fillna(0)
        df_filtered['PP_Profit_Ratio'] = (df_filtered['PP_Profit'] / df_filtered['PP_Sales']).fillna(0)

        # Create overview dataframe
        aggregation_fields = {
            'Total_Sales': df_filtered['Sales'].sum(),
            'Total_Profit': df_filtered['Profit'].sum(),
            'Average_Days_to_Ship': df_filtered['Days to Ship'].mean(),
            'PP_Total_Sales': df_filtered['PP_Sales'].sum(),
            'PP_Total_Profit': df_filtered['PP_Profit'].sum(),
            'PP_Average_Days_to_Ship': df_filtered['PP_Days_to_Ship'].mean(),
            'Total_Records': len(df_filtered),
        }

        df_overview = pd.DataFrame(aggregation_fields, index=[0])
        df_overview['Profit Ratio'] = df_overview['Total_Profit'] / df_overview['Total_Sales']
        df_overview['PP_Profit_Ratio'] = df_overview['PP_Total_Profit'] / df_overview['PP_Total_Sales']

        # Create dataframe for regional breakdowns
        df_filtered_region = filter_and_aggregate(df, 'Region', start_date, end_date)
        df_filtered_region['Profit Ratio'] = df_filtered_region['Profit'] / df_filtered_region['Sales']

        # Create dataframes for category and segment breakdowns
        df_filtered_category = filter_and_aggregate(df, 'Category', start_date, end_date)
        df_filtered_segment = filter_and_aggregate(df, 'Segment', start_date, end_date)
    else:
        raise PreventUpdate

    # Assign variables for current and previous periods
    cp_total_sales = df_overview['Total_Sales'].iloc[0]
    cp_total_profit = df_overview['Total_Profit'].iloc[0]
    cp_profit_ratio = df_overview['Profit Ratio'].iloc[0]
    cp_avg_days_to_ship = df_overview['Average_Days_to_Ship'].iloc[0]
    pp_total_sales = df_overview['PP_Total_Sales'].iloc[0]
    pp_total_profit = df_overview['PP_Total_Profit'].iloc[0]
    pp_profit_ratio = df_overview['PP_Profit_Ratio'].iloc[0]
    pp_average_days_to_ship = df_overview['PP_Average_Days_to_Ship'].iloc[0]

    # Create figures with both indicator and line chart
    def create_combined_figure(df, value_col, pp_col, title, value, reference, prefix="", suffix="",
                               color=COLOR_PRIMARY):
        # Create figure with secondary y-axis
        fig = go.Figure()

        # Add indicator
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=value,
            number={"prefix": prefix, "suffix": suffix},
            delta={"reference": reference, "valueformat": ".2f"},
            title={"text": title, "font": {"size": 16}},
            domain={'y': [0.6, 1], 'x': [0, 1]}
        ))

        # Add line chart
        fig.add_trace(go.Scatter(
            x=df['Order Date'],
            y=df[value_col],
            name="Current",
            line=dict(color=color),
            yaxis="y2"
        ))

        # Add previous period line
        fig.add_trace(go.Scatter(
            x=df['Order Date'],
            y=df[pp_col],
            name="Previous",
            line=dict(color='gray', dash='dot'),
            yaxis="y2"
        ))

        fig.update_layout(
            template='plotly_white',
            margin=dict(l=20, r=20, t=60, b=20),
            height=300,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis2=dict(
                anchor="x",
                overlaying="y",
                side="right",
                showgrid=False
            ),
            yaxis=dict(showgrid=False, showticklabels=False)
        )

        return fig

    # Sales figure
    fig_overview_1 = create_combined_figure(
        df_filtered, 'Sales', 'PP_Sales',
        "Total Sales", cp_total_sales, pp_total_sales,
        "$", "", COLOR_PRIMARY
    )

    # Profit figure
    fig_overview_2 = create_combined_figure(
        df_filtered, 'Profit', 'PP_Profit',
        "Total Profit", cp_total_profit, pp_total_profit,
        "$", "", COLOR_SECONDARY
    )

    # Profit Ratio figure
    fig_overview_3 = create_combined_figure(
        df_filtered, 'Profit Ratio', 'PP_Profit_Ratio',
        "Profit Ratio", cp_profit_ratio * 100, pp_profit_ratio * 100,
        "", "%", COLOR_SUCCESS
    )

    # Days to Ship figure
    fig_overview_4 = create_combined_figure(
        df_filtered, 'Days to Ship', 'PP_Days_to_Ship',
        "Avg Days to Ship", cp_avg_days_to_ship, pp_average_days_to_ship,
        "", " days", COLOR_DANGER
    )

    # Regional breakdown figures
    def create_bar_figure(df, x, y, title, color_scale, text, color_discrete=None):
        fig = px.bar(
            data_frame=df,
            x=x,
            y=y,
            text=text,
            color=y if color_discrete else None,
            color_discrete_sequence=color_discrete if color_discrete else None,
            color_continuous_scale=color_scale if not color_discrete else None,
            orientation="h",
            title=title
        )
        fig.update_layout(
            template='plotly_white',
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,
            showlegend=False
        )
        fig.update_traces(textposition="inside")
        return fig

    fig_overview_5 = create_bar_figure(
        df_filtered_region, 'Sales', 'Region', '',
        px.colors.diverging.Picnic, round(df_filtered_region['Sales'], 2),
        color_discrete=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_DANGER]
    )

    fig_overview_6 = create_bar_figure(
        df_filtered_region, 'Profit', 'Region', '',
        px.colors.diverging.Picnic, round(df_filtered_region['Profit'], 2),
        color_discrete=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_DANGER]
    )

    fig_overview_7 = create_bar_figure(
        df_filtered_region, df_filtered_region['Profit Ratio'] * 100, 'Region',
        '', px.colors.diverging.Picnic,
        round(df_filtered_region['Profit Ratio'] * 100, 2),
        color_discrete=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_DANGER]
    )

    fig_overview_8 = create_bar_figure(
        df_filtered_region, 'Days to Ship', 'Region',
        '', px.colors.diverging.Picnic,
        round(df_filtered_region['Days to Ship'], 2),
        color_discrete=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_DANGER]
    )

    # Pie chart figures
    def create_pie_figure(df, values, names, title, color_sequence):
        fig = px.pie(
            df,
            values=values,
            names=names,
            hole=.3,
            title=title,
            color_discrete_sequence=color_sequence
        )
        fig.update_layout(
            template='plotly_white',
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,
            showlegend=True
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    fig_overview_9 = create_pie_figure(
        df_filtered_category, 'Sales', 'Category', '',
        [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS]
    )

    fig_overview_10 = create_pie_figure(
        df_filtered_segment, 'Sales', 'Segment', '',
        [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS]
    )

    return (
        fig_overview_1, fig_overview_2, fig_overview_3, fig_overview_4,
        fig_overview_5, fig_overview_6, fig_overview_7, fig_overview_8,
        fig_overview_9, fig_overview_10
    )