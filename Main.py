# Jared Kaiser & Bryce Bales
# UCS and DFS Webtutor
# Last Updated 4/20/2023

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from igraph import Graph, Layout

# UCS and DFS algorithms
def ucs(graph, start):
    visited = set()
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            neighbors = set(graph.neighbors(vertex)) - visited
            for neighbor in neighbors:
                queue.append((neighbor, path + [neighbor]))
        yield path

def dfs(graph, start):
    visited = set()
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            neighbors = set(graph.neighbors(vertex)) - visited
            for neighbor in neighbors:
                stack.append((neighbor, path + [neighbor]))
        yield path

# Generate the graph
nr_vertices = 25
G = Graph.Tree(nr_vertices, 2)  # 2 stands for children number
layout = G.layout_reingold_tilford(root=[0])

position = {k: layout[k] for k in range(nr_vertices)}
Y = [layout[k][1] for k in range(nr_vertices)]
M = max(Y)

es = G.es  # sequence of edges
E = [e.tuple for e in es]  # list of edges

L = len(position)
Xn = [position[k][0] for k in range(L)]
Yn = [2 * M - position[k][1] for k in range(L)]
Xe = []
Ye = []
for edge in E:
    Xe += [position[edge[0]][0], position[edge[1]][0], None]
    Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

labels = [str(i) for i in range(nr_vertices)]  # Labels for nodes

# Create Plotly Traces
graph_fig = go.Figure()
graph_fig.add_trace(go.Scatter(x=Xe, y=Ye, mode='lines', line=dict(color='rgb(210,210,210)', width=1), hoverinfo='none'))
graph_fig.add_trace(go.Scatter(x=Xn, y=Yn, mode='markers', name='Nodes',
                               marker=dict(symbol='circle-dot', size=18, color='#6175c1',
                                           line=dict(color='rgb(50,50,50)', width=1)),
                               text=labels, hoverinfo='text', opacity=0.8))

# Create Text Inside the Circle via Annotations
def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
    annotations = []
    for k in range(len(pos)):
        annotations.append(dict(text=text[k], x=pos[k][0], y=2 * M - pos[k][1], xref='x1', yref='y1',
                                font=dict(color=font_color, size=font_size), showarrow=False))
    return annotations

# Add Axis Specifications and Create the Layout
axis = dict(showline=False, zeroline=False, showgrid=False, showticklabels=False)

graph_fig.update_layout(title='DFS-UCS_WebTutor', annotations=make_annotations(position, labels),
                        font_size=12, showlegend=False, xaxis=axis, yaxis=axis,
                        margin=dict(l=40, r=40, b=85, t=100), hovermode='closest',
                        plot_bgcolor='rgb(248,248,248)')

# Initialize Dash app
app = dash.Dash(__name__)

# Initialize paths_gen outside the callback
paths_gen = None
button_id = None

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Tree Plot"),
    html.H2("Depth-First Search (DFS)"),
    html.P([
            "Great reference "
            "Great reference "
            "Great reference"
    ]),
    html.P([
            "Source: ",
            html.A("This should be a source", href="ThisShouldBealink.com", target="_blank")
    ]),
    html.H2("Depth-First Search (DFS)"),
    html.P([
            "Great reference "
            "Great reference "
            "Great reference"
    ]),
    html.P([
            "Source: ",
            html.A("This should be a source", href="ThisShouldBealink.com", target="_blank")
    ]),
    html.Button('Run UCS', id='btn-ucs', n_clicks=0),
    html.Button('Run DFS', id='btn-dfs', n_clicks=0),
    dcc.Graph(id='tree-plot', figure=graph_fig),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # 1 second in milliseconds
        n_intervals=0
    )
    
])

# Define callbacks to run algorithms and update the graph
@app.callback(
    Output('tree-plot', 'figure'),
    [Input('interval-component', 'n_intervals')],
    [Input('btn-ucs', 'n_clicks'), Input('btn-dfs', 'n_clicks')],
)
def update_figure(n_intervals, n_clicks_ucs, n_clicks_dfs):
    global paths_gen, button_id  # Ensure we're modifying the global variables
    try:
        ctx = dash.callback_context
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if paths_gen is None:  # Check if paths_gen is None and initialize it
            pass

        if button_id == 'btn-ucs':
            paths_gen = ucs(G, 0)
        elif button_id == 'btn-dfs':
            paths_gen = dfs(G, 0)
        
        updated_fig = go.Figure()

        path = next(paths_gen, None)
        if path:
            highlighted_nodes = path
            highlighted_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        else:
            highlighted_nodes = []
            highlighted_edges = []

        # Add original traces
        updated_fig.add_trace(go.Scatter(x=Xe, y=Ye, mode='lines', line=dict(color='rgb(210,210,210)', width=1), hoverinfo='none'))
        updated_fig.add_trace(go.Scatter(x=Xn, y=Yn, mode='markers', name='Nodes',
                                         marker=dict(symbol='circle-dot', size=18, color='#6175c1',
                                                     line=dict(color='rgb(50,50,50)', width=1)),
                                         text=labels, hoverinfo='text', opacity=0.8))

        # Update traces based on highlighted nodes and edges
        for node in highlighted_nodes:
            updated_fig.add_trace(go.Scatter(x=[position[node][0]], 
                                             y=[2 * M - position[node][1]],
                                             mode='markers',
                                             marker=dict(color='red', size=18),
                                             text=str(node),
                                             hoverinfo='text'))

        for edge in highlighted_edges:
            updated_fig.add_trace(go.Scatter(x=[position[edge[0]][0], position[edge[1]][0]], 
                                            y=[2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1]],
                                            mode='lines',
                                            line=dict(color='red', width=2)))

        # Update layout
        updated_fig.update_layout(title='DFS-UCS_WebTutor', annotations=make_annotations(position, labels),
                                  font_size=12, showlegend=False, xaxis=axis, yaxis=axis,
                                  margin=dict(l=40, r=40, b=85, t=100), hovermode='closest',
                                  plot_bgcolor='rgb(248,248,248)')

        return updated_fig
    except Exception as e:
        print(str(e))
        return graph_fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
