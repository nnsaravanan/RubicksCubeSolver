
from functools import reduce
import plotly.graph_objects as go
from math import sqrt



def plot_cube_n(facelets=None, n=None):
    
    # Ensuring a base case if no parameters are provided
    if facelets is None and n is None:
        n = 3

    # If the facelets are given as a string with ";" as a separator, we split them
    if type(facelets) == str and ";" in facelets:
        facelets = facelets.split(";")

    # Initalizing the facelets as a solved cube if they are not given
    elif facelets is None:
        fs = n**2       # Number of facelets per face
        facelets = [*["A"]*fs, *["B"]*fs, *["C"]*fs, *["D"]*fs, *["E"]*fs, *["F"]*fs]

    # If the number of facelets is not given, we calculate it from the number of facelets
    if n == None:
        if len(facelets) % 6 != 0:
            raise Exception("The number of facelets must be a multiple of 6")
        n = int(sqrt(len(facelets) / 6))

    fs = n**2       # Number of facelets per face
    vs = (n+1)**2   # Number of vertices per face        
    
    # Vertices x, y, z coordinates for each face
    vertices = [(x, y, 0) for y in range(n, -1, -1) for x in range(n+1)]        # dn down
    vertices.extend([(x, 0, z) for z in range(n+1) for x in range(n+1)])        # f0 front
    vertices.extend([(n, y, z) for z in range(n+1) for y in range(n+1)])        # r0 right
    vertices.extend([(x, n, z) for z in range(n+1) for x in range(n, -1, -1)])  # fn back
    vertices.extend([(0, y, z) for z in range(n+1) for y in range(n, -1, -1)])  # r0 left
    vertices.extend([(x, y, n) for y in range(n+1) for x in range(n+1)])        # d0 up    - bug corrected thanks to @bminaiev here

    # Assigning colors for each letter (for the standard Rubik's cube color scheme with one color per face)
    colors = {
        "A": "white",
        "B": "#3588cc",
        "C": "red",
        "D": "green",
        "E": "orange",
        "F": "yellow",
    }

    # Building a list of colors for each facelet, as every facelet is built by two triangles, we need to repeat the color twice
    facelet_colors = [colors[facelet] for facelet in facelets]
    facecolor = []
    for f_color in facelet_colors:
        facecolor.extend([f_color, f_color])

    # Building the mesh for the cube with triangles made out of 3 vertices (i, j, k) and each facelet is made out of 2 triangles
    ivs = []
    for i in range(vs):
        if (i+1) % (n+1) != 0 and i+1 < n*(n+1): ivs.extend([i, i])

    jvs = []
    for i, j in zip([i for i in range(vs) if i % (n+1) != 0 and i < n*(n+1)], [j for j in range(vs) if (j+1) % (n+1) != 0 and j+1 > n+1]):
        jvs.extend([i, j])

    kvs = []
    for i in range(vs):
        if (i) % (n+1) != 0 and i+1 > n+1: kvs.extend([i, i])

    fig = go.Figure(data=[
        go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=reduce(lambda x, y: x.extend(y) or x, [[v+vs*i for v in ivs]for i in range(6)]),
            j=reduce(lambda x, y: x.extend(y) or x, [[v+vs*i for v in jvs]for i in range(6)]),
            k=reduce(lambda x, y: x.extend(y) or x, [[v+vs*i for v in kvs]for i in range(6)]),
            facecolor=facecolor,
            opacity=1,
            hoverinfo='none'
        )
    ])

    # Adding the black lines to the cube
    lines_seq = [[0, n, n, 0, 0], [0, 0, n, n, 0]]

    for i in range(n+1):
        # Z axis lines
        fig.add_trace(go.Scatter3d(
            x=lines_seq[0],
            y=lines_seq[1],
            z=[i]*5,
            mode="lines",
            line=dict(width=5, color="black"),
            hoverinfo="none"
        ))

        # Z axis lines
        fig.add_trace(go.Scatter3d(
            x=lines_seq[1],
            y=[i]*5,
            z=lines_seq[0],
            mode="lines",
            line=dict(width=5, color="black"),
            hoverinfo="none"
        ))

        # X axis lines
        fig.add_trace(go.Scatter3d(
            x=[i]*5,
            y=lines_seq[1],
            z=lines_seq[0],
            mode="lines",
            line=dict(width=5, color="black"),
            hoverinfo="none"
        ))

    # Adding the axis texts
    fig.add_trace(go.Scatter3d(
        x=[n/2, n/2, n+1.5+n*0.5], 
        y=[n/2, -1.5-n*0.5, n/2], 
        z=[n+1+n*0.5, n/2, n/2], 
        mode="text", 
        text=["UP", "FRONT", "RIGHT"], 
        textposition="middle center", 
        textfont=dict(
            size=15+n*2,
        )
    ))

    # Setting the layout and removing the legend, background, grid, ticks, etc.
    fig.update_layout(
        showlegend=False,
        autosize=False,
        width=900,
        height=800,
        scene=dict(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showbackground=False, title_text="", showspikes=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showbackground=False, title_text="", showspikes=False),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showbackground=False, title_text="", showspikes=False),
            camera=dict(
                eye=dict(x=0.8, y=-1.2, z=0.8)
            )
        )
    )

    fig.show()

facelets9 = "A;"*9+"C;"*9+"D;"*9+"B;"*9+"E;"*9+"F;"*9
facelets9 = facelets9[:-1]

plot_cube_n(facelets9)