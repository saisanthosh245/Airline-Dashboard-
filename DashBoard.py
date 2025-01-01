import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
data = pd.read_csv('Airline_Passenger_Data_India.csv')
data['Booking Date'] = pd.to_datetime(data['Booking Date'])
data['Flight Date'] = pd.to_datetime(data['Flight Date'])

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Airline Passenger Dashboard", style={'textAlign': 'center'}),

    html.Div([
        dcc.Dropdown(
            id='time-period-filter',
            options=[
                {'label': 'Last 7 Days', 'value': '7D'},
                {'label': 'Last 1 Month', 'value': '1M'},
                {'label': 'Last 1 Year', 'value': '1Y'}
            ],
            value='7D',
            placeholder="Select Time Period",
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    dcc.Graph(id='bar-graph'),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='line-graph'),
    dcc.Graph(id='bubble-chart')
])

# Callbacks
@app.callback(
    [
        Output('bar-graph', 'figure'),
        Output('pie-chart', 'figure'),
        Output('line-graph', 'figure'),
        Output('bubble-chart', 'figure')
    ],
    [Input('time-period-filter', 'value')]
)
def update_dashboard(time_period):
    # Define time period filter
    if time_period == '7D':
        start_date = data['Booking Date'].max() - pd.Timedelta(days=7)
    elif time_period == '1M':
        start_date = data['Booking Date'].max() - pd.DateOffset(months=1)
    elif time_period == '1Y':
        start_date = data['Booking Date'].max() - pd.DateOffset(years=1)

    filtered_data = data[data['Booking Date'] >= start_date]

    # Bar Graph: Number of travelers in each class
    bar_data = filtered_data.groupby('Travel Class')['PassengerID'].count().reset_index()
    bar_fig = px.bar(bar_data, x='Travel Class', y='PassengerID', color='Travel Class',
                     title="Number of Travelers by Class")

    # Pie Chart: Gender distribution across travel classes
    pie_data = filtered_data.groupby('Gender')['PassengerID'].count().reset_index()
    pie_fig = px.pie(pie_data, names='Gender', values='PassengerID', title="Gender Distribution")

    # Line Graph: Trend of bookings over time
    line_data = filtered_data.groupby('Booking Date').size().reset_index(name='Booking Count')
    line_fig = px.line(line_data, x='Booking Date', y='Booking Count', title="Booking Trend Over Time")

    # Bubble Chart: Class, Gender, and Fare distribution
    bubble_fig = px.scatter(filtered_data, x='Travel Class', y='Fare', size='Fare', color='Gender',
                             hover_data=['PassengerID', 'Booking Date'],
                             title="Bubble Chart: Class, Gender, and Fare")

    return bar_fig, pie_fig, line_fig, bubble_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)