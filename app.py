from dash import Dash, dcc, html
from layouts import create_layout
from callbacks import register_callbacks
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = Dash(__name__)

# Load the GDP vs Life Expectancy dataset
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

# Create the scatter plot
gdp_life_fig = px.scatter(
    df, x="gdp per capita", y="life expectancy",
    size="population", color="continent", hover_name="country",
    log_x=True, size_max=60
)

# Set the app layout
app.layout = create_layout(gdp_life_fig)

# Register callbacks
register_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)