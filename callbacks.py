from dash import Input, Output
import plotly.express as px
import pandas as pd

def register_callbacks(app):
    @app.callback(
        Output('metric-graph', 'figure'),
        [Input('metric-dropdown', 'value')]
    )
    def update_graph(selected_metric):
        # Sample data (replace with your actual data)
        if selected_metric == 'sales':
            df = pd.DataFrame({
                'Year': [2019, 2020, 2021, 2022, 2023],
                'Sales': [100000, 120000, 150000, 180000, 200000]
            })
            fig = px.line(df, x='Year', y='Sales', title='Sales Trends Over Time')
        elif selected_metric == 'demographics':
            df = pd.DataFrame({
                'Region': ['North', 'South', 'East', 'West'],
                'Customers': [500, 300, 400, 600]
            })
            fig = px.bar(df, x='Region', y='Customers', title='Customer Demographics by Region')
        elif selected_metric == 'products':
            df = pd.DataFrame({
                'Product': ['A', 'B', 'C', 'D'],
                'Revenue': [25000, 30000, 20000, 35000]
            })
            fig = px.pie(df, names='Product', values='Revenue', title='Product Performance by Revenue')
        return fig