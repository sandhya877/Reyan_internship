import dash
from dash import dcc, html
from dash.dash_table import DataTable

from dash.dependencies import Input, Output
import pandas as pd
import psycopg2
import plotly.express as px

# Replace with your PostgreSQL database credentials
db_connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="password"
)

# Define the query to retrieve the data from the PostgreSQL table
query = "SELECT * FROM monthlyreport_eh_mod_final;"

# Load the data into a DataFrame
df = pd.read_sql(query, db_connection)

# Initialize the Dash web application
app = dash.Dash(__name__)

# Define the Dash layout
app.layout = html.Div([
    html.H1("Electronics Hub - Month over Month Traffic Report"),
    
    dcc.Dropdown(
        id='column-selector',
        options=[{'label': col, 'value': col} for col in df.columns],
        multi=True
    ),
    DataTable(
        id='data-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        page_size=100,  # Show 100 rows per page
        style_cell={'textAlign': 'left'},  # Align cell text to the left
        style_header={'fontWeight': 'bold'},  # Make column headers bold
        style_table={'height': '800px', 'overflowY': 'auto'},  # Add scrollability
        sort_action='native',  # Enable native sorting
        sort_mode='multi',    # Allow multiple column sorting
       
        filter_action='native',  # Enable native column filtering
        filter_query='', 
    ),
    
    # html.Style({'selector': '.column-header[data-column="pageTitle"]', 'style': {'min-width': '100px'}}),

    
])


# Define callback to apply background color for columns ending with 'Change'
@app.callback(
    Output('data-table', 'style_data_conditional'),
    Input('column-selector', 'value')
)

def color_code_changes(selected_columns):
    if not selected_columns:
        selected_columns = df.columns

    style_data_conditional = []

    for col in selected_columns:
        if col.endswith('%'):
            style_data_conditional.append(
                {
                    'if': {
                        'column_id': col,
                        'filter_query': '{' + col + '} > 0',
                    },
                    'backgroundColor': '#39E75F',
                    'color': 'black',  # Font color for positive values
                }
            )
            style_data_conditional.append(
                {
                    'if': {
                        'column_id': col,
                        'filter_query': '{' + col + '} < 0',
                    },
                    'backgroundColor': '#FF4F4B',
                    'color': 'black',  # Font color for negative values
                }
            )

    return style_data_conditional

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
