from dash import dcc, html

def create_layout(gdp_life_fig):
    return html.Div([
        html.H1("AdventureWorks Dashboard", style={'textAlign': 'center'}),
        
        # Dropdown for selecting metrics
        html.Label("Select Metric:"),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Sales Trends', 'value': 'sales'},
                {'label': 'Customer Demographics', 'value': 'demographics'},
                {'label': 'Product Performance', 'value': 'products'}
            ],
            value='sales'
        ),
        
        # Graph for AdventureWorks metrics
        dcc.Graph(id='metric-graph'),
        
        # Separator
        html.Hr(),
        
        # GDP vs Life Expectancy scatter plot
        html.H2("Sales Trends vs Product Performance", style={'textAlign': 'center'}),
        dcc.Graph(
            id='gdp-life-exp',
            figure=gdp_life_fig
        )
    ])