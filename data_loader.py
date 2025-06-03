from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import pyodbc

# Connect to AdventureWorks database
def connect_to_db():
    conn_str = (
        r"DRIVER={SQL Server};"
        r"SERVER=DESKTOP-95S7QHM\SQLEXPRESS;"  # Replace with your server name
        r"DATABASE=AdventureWorks2019;"
        r"UID=your_username;"  # Replace with your username
        r"PWD=your_password;"  # Replace with your password
    )
    conn = pyodbc.connect(conn_str)
    return conn

# Load data from AdventureWorks
def load_sales_data():
    conn = connect_to_db()
    query = """
    SELECT 
        YEAR(OrderDate) AS Year,
        SUM(TotalDue) AS TotalSales
    FROM Sales.SalesOrderHeader
    GROUP BY YEAR(OrderDate)
    ORDER BY Year
    """
    df_sales = pd.read_sql(query, conn)
    conn.close()
    return df_sales

def load_customer_data():
    conn = connect_to_db()
    query = """
    SELECT 
        TerritoryID,
        COUNT(CustomerID) AS CustomerCount
    FROM Sales.Customer
    GROUP BY TerritoryID
    """
    df_customers = pd.read_sql(query, conn)
    conn.close()
    return df_customers

def load_product_data():
    conn = connect_to_db()
    query = """
    SELECT 
        ProductCategory.Name AS Category,
        SUM(SalesOrderDetail.LineTotal) AS TotalRevenue
    FROM Sales.SalesOrderDetail
    INNER JOIN Production.Product ON SalesOrderDetail.ProductID = Product.ProductID
    INNER JOIN Production.ProductSubcategory ON Product.ProductSubcategoryID = ProductSubcategory.ProductSubcategoryID
    INNER JOIN Production.ProductCategory ON ProductSubcategory.ProductCategoryID = ProductCategory.ProductCategoryID
    GROUP BY ProductCategory.Name
    """
    df_products = pd.read_sql(query, conn)
    conn.close()
    return df_products

# Load data
df_sales = load_sales_data()
df_customers = load_customer_data()
df_products = load_product_data()

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("AdventureWorks 2019 Dashboard", style={'textAlign': 'center'}),

    # Dropdown for selecting metrics
    html.Div([
        html.Label("Select Metric:"),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Sales Trends', 'value': 'sales'},
                {'label': 'Customer Demographics', 'value': 'customers'},
                {'label': 'Product Performance', 'value': 'products'}
            ],
            value='sales'
        )
    ], style={'width': '49%', 'margin': 'auto'}),

    # Graph container
    dcc.Graph(id='metric-graph')
])

# Callback to update the graph
@callback(
    Output('metric-graph', 'figure'),
    Input('metric-dropdown', 'value')
)
def update_graph(selected_metric):
    if selected_metric == 'sales':
        fig = px.line(df_sales, x='Year', y='TotalSales', title='Sales Trends Over Time')
    elif selected_metric == 'customers':
        fig = px.bar(df_customers, x='TerritoryID', y='CustomerCount', title='Customer Demographics by Territory')
    elif selected_metric == 'products':
        fig = px.pie(df_products, names='Category', values='TotalRevenue', title='Product Performance by Revenue')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)