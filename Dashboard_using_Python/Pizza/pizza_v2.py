import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

# Load the data
file_path =  'Pizza_Chart1.xlsx'  # Ensure this is the correct path to your file
df = pd.read_excel(file_path)

# Ensure there are no null values in the 'Pizza Type' column
df = df.dropna(subset=['Pizza Type'])

# Initialize the Dash app
app = Dash(__name__)

# Layout of the Dashboard
app.layout = html.Div([
    html.H1("Pizza Data Analysis Dashboard"),
    
    html.H3("Select Pizza Types to View in Pie Chart"),
    dcc.Checklist(
        id='pizza-type-checkbox',
        options=[{'label': pizza_type, 'value': pizza_type} for pizza_type in df['Pizza Type'].unique()],
        value=df['Pizza Type'].unique().tolist(),
        labelStyle={'display': 'inline-block'}
    ),
    
    dcc.Graph(id='pizza-pie-chart'),
    
    html.H3("Select Pizza Types to Compare in Bar Chart"),
    dcc.Dropdown(
        id='pizza-dropdown',
        options=[{'label': pizza_type, 'value': pizza_type} for pizza_type in df['Pizza Type'].unique()],
        multi=True,
        value=df['Pizza Type'].unique().tolist(),
        placeholder="Select Pizza Types"
    ),
    
    dcc.Graph(id='pizza-bar-chart'),

    html.H3("Analyze Pizza Data by Size"),
    dcc.Dropdown(
        id='pizza-size-dropdown',
        options=[{'label': pizza_type, 'value': pizza_type} for pizza_type in df['Pizza Type'].unique()],
        multi=True,
        value=df['Pizza Type'].unique().tolist(),
        placeholder="Select Pizza Types for Size Analysis"
    ),
    dcc.Graph(id='pizza-size-analysis')  # New graph for pizza size analysis
])

# Callback to update the pie chart based on selected pizza types
@app.callback(
    Output('pizza-pie-chart', 'figure'),
    [Input('pizza-type-checkbox', 'value')]
)
def update_pie_chart(selected_pizzas):
    if not selected_pizzas:
        return px.pie(title='No pizza type selected')
    
    filtered_df = df[df['Pizza Type'].isin(selected_pizzas)]
    fig = px.pie(filtered_df, names='Pizza Type', values='Number of People Who Liked It', title='Pizza Popularity')
    return fig

# Callback to update the bar chart based on selected pizza types
@app.callback(
    Output('pizza-bar-chart', 'figure'),
    [Input('pizza-dropdown', 'value')]
)
def update_bar_chart(selected_pizzas):
    if selected_pizzas is None or len(selected_pizzas) == 0:
        filtered_df = df
    else:
        filtered_df = df[df['Pizza Type'].isin(selected_pizzas)]
    
    fig = px.bar(filtered_df, x='Pizza Type', y='Number of People Who Liked It', color='Crust Type', barmode='group',
                 title='Detailed Pizza Analysis', text='Size')
    return fig

# Callback to update the pizza size analysis graph
@app.callback(
    Output('pizza-size-analysis', 'figure'),
    [Input('pizza-size-dropdown', 'value')]
)
def update_size_analysis(selected_pizzas):
    if selected_pizzas is None or len(selected_pizzas) == 0:
        return px.scatter(title='No pizza type selected')
    
    filtered_df = df[df['Pizza Type'].isin(selected_pizzas)]
    fig = px.bar(filtered_df, x='Size', y='Number of People Who Liked It', color='Pizza Type', barmode='group',
                 title='Pizza Size Analysis')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
