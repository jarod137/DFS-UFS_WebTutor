import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
import igraph
from igraph import Graph, Layout
import plotly.graph_objects as go
import time

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

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Tree Plot"),
    html.Button('Run UCS', id='btn-ucs', n_clicks=0),
    html.Button('Run DFS', id='btn-dfs', n_clicks=0),
    dcc.Graph(id='tree-plot', figure=graph_fig),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # in milliseconds
        n_intervals=0
    )
])

# Initialize paths_gen outside the callback
paths_gen = None

# Define callbacks to run algorithms and update the graph
@app.callback(
    Output('tree-plot', 'figure'),
    [Input('interval-component', 'n_intervals')],
    [State('btn-ucs', 'n_clicks'), State('btn-dfs', 'n_clicks')]
)
def update_figure(n_intervals, n_clicks_ucs, n_clicks_dfs):
    global paths_gen  # Ensure we're modifying the global variable
    try:
        ctx = dash.callback_context
        button_id = 'btn-ucs'  # default to UCS
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'btn-ucs':
            paths_gen = ucs(G, 0)
        elif button_id == 'btn-dfs':
            paths_gen = dfs(G, 0)
        
        path = next(paths_gen, None)
        if path:
            highlighted_nodes = path
            highlighted_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        else:
            highlighted_nodes = []
            highlighted_edges = []

        updated_fig = graph_fig.update_traces(marker=dict(color='#6175c1'), line=dict(color='rgb(210,210,210)', width=1))

        for node in highlighted_nodes:
            updated_fig.update_traces(marker=dict(color='red'), selector=dict(text=str(node)))

        for edge in highlighted_edges:
            updated_fig.add_trace(go.Scatter(x=[position[edge[0]][0], position[edge[1]][0]], 
                                            y=[2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1]],
                                            mode='lines',
                                            line=dict(color='red', width=2)))
        return updated_fig
    except Exception as e:
        print(str(e))
        return graph_fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
