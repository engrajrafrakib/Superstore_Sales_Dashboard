# This page gives the general overview of different properties to analyze the sales data.
# Import required modules
from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from main import *

# Create a list of columns, those are required for the landing page.
column_list = ['Order Date','Sales','Profit', 'Days to Ship', 'Region', 'Category', 'Segment']
# Create page specific initial dataframe.
df = df_main[column_list]

# Designing page layout by initializing different blocks/sections.
# Design the page header/title block.
page_header = dbc.CardGroup([
    dcc.Store(id='store-data', data=[], storage_type='memory'),
    dbc.Card(
            dbc.CardBody([
                    html.H3("Landing Page", className="card-title", style={"font-size":30}),
                    html.P("General overview of the Sales Data.", className="card-text")
                    ])
            ),
        dbc.Card(
            html.Div(className="fa-solid fa-house-user", style={"color": "white","textAlign": "center","fontSize": 24,"margin": "auto"}),
            className="bg-primary",
            style={"maxWidth": 75}
            )], className="mt-4 shadow"
                            )
# Design the date-filter block.
selection_filter = dbc.Card(
    dbc.CardBody([
        html.Label('Start / End Date'),
        dbc.Col([
            dcc.DatePickerRange(
                id='date-range-picker',
                start_date='2017-01-01',
                end_date='2017-12-31',
                display_format='DD/MM/YYYY',
                # style={'width':'100%', 'text-align':'center', 'border':'0px', 'background-color': 'transparent', 'margin': '0%'},
                )
            ])
        ]),
    style={'width':'100%', 'text-align':'center', 'border':'0px', 'background-color': 'transparent'}
    )
            
# Design overview graphs/charts block.
# Overview charts, one to visualize the comparison between current period (CP) and previous period (PP) sales, another to visualize sales by region. 
overview_chart_1 = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='overview-sales', figure=go.Figure()),
        dcc.Graph(id='overview-sales-by-region', figure=go.Figure())
        ])
    # style={'width': '50%', 'display': 'inline-block', 'float': 'left', 'color': '#17B897', 'text-alignment': 'left', 'margin-left': '25%', 'margin-right': '25%'}
    )
# Overview charts, one to visualize the comparison between current period (CP) and previous period (PP) profit, another to visualize profit by region
overview_chart_2 = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='overview-profit', figure=go.Figure()),
        dcc.Graph(id='overview-profit-by-region', figure=go.Figure())
        ])
    )
# Overview charts, one to visualize the comparison between current period (CP) and previous period (PP) profit ratio, another to visualize profit ratio by region.
overview_chart_3 = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='overview-profit-ratio', figure=go.Figure()),
        dcc.Graph(id='overview-profit-ratio-by-region', figure=go.Figure())
        ])
    )
# Overview charts, one to visualize the comparison between current period (CP) and previous period (PP) average days to ship, another to visualize average days to ship.
overview_chart_4 = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='overview-average-days-to-ship', figure=go.Figure()),
        dcc.Graph(id='overview-average-days-to-ship-by-region', figure=go.Figure())
        ])
    )
# Overview chart to visualize the sales percentage by category and a cardlink to redirect to the datatable page.
overview_chart_5 = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='overview-sales-by-category', figure=go.Figure()),
        dbc.CardLink("View DataTable", href="/pages/table")
        ])
    )
# Overview chart to visualize the sales percentage by segment and a cardlink to redirect to the graph page.
overview_chart_6 = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='overview-sales-by-segment', figure=go.Figure()),
        dbc.CardLink("View Graphs", href="/pages/graph", style={'float': 'right'})
        ]),  
    #style={'width': '50%', 'display': 'inline-block', 'float': 'left', 'color': '#17B897', 'text-alignment': 'left', 'margin-left': '25%', 'margin-right': '25%'}

    )

# Structuring the main layout of the page.
layout = html.Div([
    # Page title/header
    dbc.Row([
        dbc.Col(page_header, width=12),
    ], justify="center"),
    # Date filter to select date range.
    dbc.Row([
        dbc.Col(selection_filter, width={"size": 4, "offset": 4}),
    ]),
    # First chart block. This block contains in total four scatter charts and four bar charts.
    dbc.Row([
        dbc.Col(overview_chart_1, width=3),
        dbc.Col(overview_chart_2, width=3),
        dbc.Col(overview_chart_3, width=3),
        dbc.Col(overview_chart_4, width=3)
        ],justify="center"), 
    html.Br(),
    # Second chart block. This block contains in total two pie charts with two card links that can 
    # communicate with datatable page and graph page. 
    dbc.Row([
        dbc.Col(overview_chart_5, width=4),
        dbc.Col(overview_chart_6, width=4),
        ], justify="center")
    ])

# Create additional dataframes by aggregating relevant information. 
def filter_and_aggregate(df, column, start_date, end_date):
    df_filtered = df[df['Order Date'].between(start_date, end_date)]
    df_filtered = df_filtered.groupby(column).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Days to Ship': 'mean'
    }).reset_index()
    return df_filtered

# Callback function to update detailed sales overview charts.
# @callback(
#     Input(component_id='overview-sales-by-region', component_property='clickData')
# )

# Callback function to update overview charts
@callback([Output('overview-sales', 'figure'), 
           Output('overview-profit', 'figure'), 
           Output('overview-profit-ratio', 'figure'), 
           Output('overview-average-days-to-ship', 'figure'),
           Output('overview-sales-by-region', 'figure'),
           Output('overview-profit-by-region', 'figure'),
           Output('overview-profit-ratio-by-region', 'figure'),
           Output('overview-average-days-to-ship-by-region', 'figure'),
           Output('overview-sales-by-category', 'figure'),
           Output('overview-sales-by-segment', 'figure'),],
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
        
        # Use Pandas shift method to estimate prior periods sales information. In this case relevant sales columns data shifted by 1 days.
        # Calculate prior period sales
        df_filtered['PP_Sales'] = df_filtered['Sales'].shift(1).fillna(0)
        # Calculate prior period profits
        df_filtered['PP_Profit'] = df_filtered['Profit'].shift(1).fillna(0)
        # Calculate prior profit ratio
        df_filtered['PP_Days_to_Ship'] = df_filtered['Days to Ship'].shift(1).fillna(0)
        # Calculate prior average days to shipping
        df_filtered['PP_Profit_Ratio'] = (df_filtered['PP_Profit'] / df_filtered['PP_Sales']).fillna(0)
        
        # Create overview dataframe by aggregating below fields from the dataset.  
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
        
        # Create dataframe to represent regional sales overview graphs.
        df_filtered_region = filter_and_aggregate(df, 'Region', start_date, end_date)
        df_filtered_region['Profit Ratio'] = df_filtered_region['Profit'] / df_filtered_region['Sales']
        
        # Create dataframe to represent sales overview by category.
        df_filtered_category = filter_and_aggregate(df, 'Category', start_date, end_date)
        # Create dataframe to represent sales overview by segment.
        df_filtered_segment = filter_and_aggregate(df, 'Segment', start_date, end_date)
    else:
        raise PreventUpdate
        
    # Assigining few variables with current period (cp) and prior period (pp) to be used in particular graph figures.
    cp_total_sales = df_overview['Total_Sales'].iloc[0]
    cp_total_profit = df_overview['Total_Profit'].iloc[0]
    cp_profit_ratio = df_overview['Profit Ratio'].iloc[0]
    cp_avg_days_to_ship = df_overview['Average_Days_to_Ship'].iloc[0]
    pp_total_sales = df_overview['PP_Total_Sales'].iloc[0]
    pp_total_profit = df_overview['PP_Total_Profit'].iloc[0]
    pp_profit_ratio = df_overview['PP_Profit_Ratio'].iloc[0]
    pp_average_days_to_ship = df_overview['PP_Average_Days_to_Ship'].iloc[0]
    
    # Sales overview figure with KPI indicator.
    fig_overview_1 = go.Figure(go.Indicator(
    mode = "number+delta",
    value = cp_total_sales,
    number = {"prefix": "$"},
    delta = {"reference": pp_total_sales, "valueformat": ".2f", "prefix":"$"},
    title = {"text": "Total Sales"},
    domain = {'y': [0.8, 1], 'x': [0.25, 0.75]}))
    fig_overview_1.add_traces(px.line(df_filtered, 
                x='Order Date', 
                y=['Sales', 'PP_Sales'], 
                title='Timeline Graph',
                labels={"value": "Total Sales", "Order Date": "Period", "variable": "Properties", "Sales":"CP_Sales"}, 
                markers=True,
                log_y=True).data)
    fig_overview_1.update_layout(xaxis = {'range': [start_date, end_date]}, template='plotly_white')
    fig_overview_1.update_xaxes(tickformat='%Y-%m-%d', ticks='outside', showline=False, linecolor='white', gridcolor='white')
    fig_overview_1.update_yaxes(ticks='outside', showline=True, linecolor='white', gridcolor='white')
    fig_overview_1.update_traces(title_font_size=20, number_font_size=20, delta_font_size=20, selector=dict(type='indicator'))
    
    # Profit overview figure with KPI indicator.
    fig_overview_2 = go.Figure(go.Indicator(
    mode = "number+delta",
    value = cp_total_profit,
    number = {"prefix": "$"},
    delta = {"reference": pp_total_profit, "valueformat": ".2f", "prefix":"$"},
    title = {"text": "Total Profit"},
    domain = {'y': [0.8, 1], 'x': [0.25, 0.75]}))
    fig_overview_2.add_traces(px.line(df_filtered, 
                x='Order Date', 
                y=['Profit', 'PP_Profit'], 
                title='Timeline Graph',
                labels={"value": "Total Profit", "Order Date": "Period", "variable": "Properties", "Profit":"CP_Profit"}, 
                markers=True,
                log_y=True).data)
    fig_overview_2.update_layout(xaxis = {'range': [start_date, end_date]}, template='plotly_white')
    fig_overview_2.update_xaxes(tickformat='%Y-%m-%d', ticks='outside', showline=False, linecolor='white', gridcolor='white')
    fig_overview_2.update_yaxes(ticks='outside', showline=True, linecolor='white', gridcolor='white')
    fig_overview_2.update_traces(title_font_size=20, number_font_size=20, delta_font_size=20, selector=dict(type='indicator'))
    
    # Profit Ratio overview figure with KPI indicator.
    fig_overview_3 = go.Figure(go.Indicator(
    mode = "number+delta",
    value = cp_profit_ratio*100,
    number = {"suffix": "%"},
    delta = {"reference": pp_profit_ratio, "valueformat": ".2f", "suffix":"%"},
    title = {"text": "Profit Ratio"},
    domain = {'y': [0.8, 1], 'x': [0.25, 0.75]}))
    fig_overview_3.add_traces(px.line(df_filtered, 
                x='Order Date', 
                y=['Profit Ratio', 'PP_Profit_Ratio'], 
                title='Timeline Graph',
                labels={"value": "Total Profit Ratio", "Order Date": "Period", "variable": "Properties", "Profit Ratio":"CP_Profit_Ratio"}, 
                markers=True,
                log_y=True).data)
    fig_overview_3.update_layout(xaxis = {'range': [start_date, end_date]}, template='plotly_white')
    fig_overview_3.update_xaxes(tickformat='%Y-%m-%d', mirror=True, ticks='outside', showline=False, linecolor='white', gridcolor='white')
    fig_overview_3.update_yaxes(mirror=True, ticks='outside', showline=True, linecolor='white', gridcolor='white')
    fig_overview_3.update_traces(title_font_size=20, number_font_size=20, delta_font_size=20, selector=dict(type='indicator'))
    
    # Average Days to Ship overview figure with KPI indicator.
    fig_overview_4 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = cp_avg_days_to_ship,
        number = {"suffix": " days"},
        delta = {"reference": pp_average_days_to_ship, "valueformat": ".2f", "suffix": " days"},
        title = {"text": "AVG Days to Ship"},
        domain = {'y': [0.8, 1], 'x': [0.25, 0.75]}))
    fig_overview_4.add_traces(px.line(df_filtered, 
                x='Order Date', 
                y=['Days to Ship', 'PP_Days_to_Ship'], 
                title='Timeline Graph',
                labels={"value": "Average Days to Ship", "Order Date": "Time Period", "variable": "Properties", "Sales":"CP_Days_to_Ship"}, 
                markers=True,
                log_y=True).data)
    fig_overview_4.update_layout(xaxis = {'range': [start_date, end_date]}, template='plotly_white')
    fig_overview_4.update_xaxes(tickformat='%Y-%m-%d', mirror=True, ticks='outside', showline=False, linecolor='white', gridcolor='white')
    fig_overview_4.update_yaxes(mirror=True, ticks='outside', showline=True, linecolor='white', gridcolor='white')
    fig_overview_4.update_traces(title_font_size=20, number_font_size=20, delta_font_size=20, delta_increasing_color ='#FF4136',delta_decreasing_color ='#3D9970', selector=dict(type='indicator'))
    
    # Regional Sales overview figure.
    fig_overview_5 = go.Figure(
        px.bar(
        data_frame=df_filtered_region,
        x='Sales',
        y='Region',
        text=round(df_filtered_region['Sales'], 2),
        color='Region',
        opacity=0.9,
        orientation="h",
        barmode="relative",
        hover_data={'Profit': True},
        color_continuous_scale=px.colors.diverging.Picnic,
        title='By Region',
        labels={"Sales": "Total Sales", "Region": "Region",  "text": "Total Sales"})
        )
    fig_overview_5.update_layout(template='plotly_white')
    fig_overview_5.update_traces(textposition="inside", showlegend=True)
    fig_overview_5.update_xaxes(mirror=True, ticks='outside', showline=False, linecolor='white', gridcolor='white', tickprefix='$')
    fig_overview_5.update_yaxes(mirror=True, ticks='outside', showline=True, linecolor='white', gridcolor='white') # , categoryorder="total ascending"
    
    # Regional Sales overview figure.
    fig_overview_6 = go.Figure(
        px.bar(
        data_frame=df_filtered_region,
        x='Profit',
        y='Region',
        text=round(df_filtered_region['Profit'], 2),
        color='Region',
        opacity=0.9,
        orientation="h",
        barmode="relative",
        hover_data={'Profit': True, 'Sales': True},
        color_continuous_scale=px.colors.diverging.Picnic,
        title='By Region',
        labels={"Profit": "Total Profit", "Region": "Region",  "text": "Total Profit"})
        )
    fig_overview_6.update_layout(template='plotly_white')
    fig_overview_6.update_traces(textposition="inside", showlegend=True)
    fig_overview_6.update_xaxes(mirror=True, ticks='outside', showline=False, linecolor='white', gridcolor='white', tickprefix='$')
    fig_overview_6.update_yaxes(mirror=True, ticks='outside', showline=False, linecolor='white', gridcolor='white')

    # Regional Profit Ratio overview figure.
    fig_overview_7 = go.Figure(
        px.bar(
        data_frame=df_filtered_region,
        x=df_filtered_region['Profit Ratio']*100,
        y='Region',
        text=round(df_filtered_region['Profit Ratio']*100, 2),
        color='Region',
        opacity=0.9,
        orientation="h",
        barmode="relative",
        hover_data={'Sales': True, 'Profit': True},
        color_continuous_scale=px.colors.diverging.Picnic,
        title='By Region',
        labels={"text": "Profit Ratio", "x":"Profit Ratio"})    
        )
    fig_overview_7.update_layout(template='plotly_white')
    fig_overview_7.update_traces(textposition="inside", showlegend=True)
    fig_overview_7.update_xaxes(mirror=True, ticks='outside', showline=False, linecolor='white', gridcolor='white', ticksuffix='%')
    fig_overview_7.update_yaxes(mirror=True, ticks='outside', showline=False, linecolor='white', gridcolor='white')
    
    # Regional Average Days to Ship overview figure.
    fig_overview_8 = go.Figure(
        px.bar(
        data_frame=df_filtered_region,
        x='Days to Ship',
        y='Region',
        text=round(df_filtered_region['Days to Ship'], 2),
        color='Region',
        opacity=0.9,
        orientation="h",
        barmode="relative",
        color_continuous_scale=px.colors.diverging.Picnic,
        title='By Region',
        labels={"text": "AVG Days to Ship", "Days to Ship":"AVG Days to Ship"})    
        )
    fig_overview_8.update_layout(template='plotly_white')
    fig_overview_8.update_traces(textposition="inside", showlegend=True)
    fig_overview_8.update_xaxes(mirror=True, ticks='outside', showline=False, linecolor='white', gridcolor='white')
    fig_overview_8.update_yaxes(mirror=True, ticks='outside', showline=False, linecolor='white', gridcolor='white')
    
    fig_overview_9 = px.pie(df_filtered_category, 
                            values='Sales',
                            names='Category',
                            hole=.3,
                            title='Sales by Category',
                            hover_data=['Sales'],
                            labels={'Sales':'Total Sales'})
    fig_overview_9.update_traces(textposition='inside', textinfo='percent')
    
    fig_overview_10 = px.pie(df_filtered_segment,
                             values='Sales',
                             names='Segment',
                             hole=.3,
                            title='Sales by Segment',
                            hover_data=['Sales'],
                            labels={'Sales':'Total Sales'})
    fig_overview_10.update_traces(textposition='inside', textinfo='percent')
    return fig_overview_1, fig_overview_2, fig_overview_3, fig_overview_4, fig_overview_5, fig_overview_6, fig_overview_7, fig_overview_8, fig_overview_9, fig_overview_10
