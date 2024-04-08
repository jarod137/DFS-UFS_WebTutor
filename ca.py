# Jared Kaiser & Bryce Bales AI Project

import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import plotly.graph_objs as go
import time

# Define graph edges
graph_edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Graph Search Visualization"),
    dcc.Graph(id='graph-visualization', figure=go.Figure()),
    html.Button('Start DFS', id='start-dfs-button', n_clicks=0),
    html.Button('Start UCS', id='start-ucs-button', n_clicks=0),
    html.Button('Reset', id='reset-button', n_clicks=0),
    html.Div(id='output')
])

# Define callback function to update the visualization based on user interactions
@app.callback(
    Output('graph-visualization', 'figure'),
    [Input('start-dfs-button', 'n_clicks'),
     Input('start-ucs-button', 'n_clicks'),
     Input('reset-button', 'n_clicks')],
    [State('graph-visualization', 'figure')]
)
def update_graph(n_clicks_dfs, n_clicks_ucs, n_clicks_reset, current_figure):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'start-dfs-button':
        if n_clicks_dfs > 0:
            # Placeholder logic for DFS algorithm
            time.sleep(1)  # Simulate algorithm execution
            new_trace = go.Scatter(x=[1, 2], y=[2, 3], mode='lines', name='DFS Path', line=dict(color='red'))
            current_figure['data'].append(new_trace)
            return current_figure
    elif button_id == 'start-ucs-button':
        if n_clicks_ucs > 0:
            # Placeholder logic for UCS algorithm
            time.sleep(1)  # Simulate algorithm execution
            new_trace = go.Scatter(x=[1, 3, 6], y=[2, 4, 5], mode='lines', name='UCS Path', line=dict(color='blue'))
            current_figure['data'].append(new_trace)
            return current_figure
    elif button_id == 'reset-button':
        if n_clicks_reset > 0:
            # Reset graph visualization
            return go.Figure(data=[], layout=go.Layout())
    return current_figure

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
