import streamlit as st
import pandas as pd
import os
import networkx as nx
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

CSV_FOLDER = "../csv"
ATTACKER_FIELD = "attackerField"
SERVER_FIELD = "serverField"

def get_all_csv_files():
    files = [os.path.join(CSV_FOLDER, f) for f in os.listdir(CSV_FOLDER) if f.endswith(".csv")]
    return files

def load_data():
    csv_files = get_all_csv_files()
    if csv_files:
        data_frames = [pd.read_csv(file) for file in csv_files]
        return pd.concat(data_frames, ignore_index=True)
    return None

def plot_network_graph(data):
    G = nx.Graph()
    node_info = {}

    for _, row in data.iterrows():
        attacker = row[ATTACKER_FIELD]
        server = row[SERVER_FIELD]
        details = f"Protocol: {row['protocol']}\nTime: {row['startDate']}"
        G.add_node(attacker, label=details, color='red', type='attacker')
        G.add_node(server, label=details, color='green', type='server')
        G.add_edge(attacker, server)
        node_info[attacker] = "Attacker"
        node_info[server] = "Server"

    pos = nx.spring_layout(G, seed=42)
    node_x, node_y, node_color, node_text, node_customdata, node_types = [], [], [], [], [], []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_color.append("red" if node_info[node] == "Attacker" else "green")
        node_text.append(node)
        node_customdata.append(G.nodes[node]['label'])
        node_types.append(G.nodes[node]['type'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode="markers+text", text=node_text,
        textposition="top center", marker=dict(size=12, color=node_color),
        hoverinfo="text", customdata=node_customdata, name="Nodes"
    ))

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines", line=dict(width=1, color="gray"),
            hoverinfo="none", showlegend=False
        ))

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title_text=""),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title_text=""),
        plot_bgcolor="white"
    )

    selected_event = plotly_events(fig, click_event=True)

    if selected_event:
        selected_node_index = selected_event[0]["pointIndex"]
        selected_node = node_text[selected_node_index]
        selected_node_type = node_types[selected_node_index]

        if selected_node_type == "server":
            attackers = data[data[SERVER_FIELD] == selected_node][ATTACKER_FIELD].unique()
            
            st.sidebar.markdown(
                f"### Node selected is a <span style='color: green;'>server</span>: {selected_node}<br><br>"
                f"It has been attacked by:<br>"
                + "<br>".join([f"<span style='color: red;'>•</span> {ip}" for ip in attackers]),
                unsafe_allow_html=True
            )
        else:
            st.sidebar.write(f"### Details for {selected_node}")
            filtered_data = data[data['attackerField'] == selected_node]
            ip_counter = 1
            for _, row in filtered_data.iterrows():
                st.sidebar.markdown(
                    f"<b>Req {ip_counter}:</b><br><b>Protocol:</b> {row['protocol']}  <br>"
                    f"<b>Start Date:</b> {row['startDate']}  <br>"
                    f"<b>End Date:</b> {row['endDate']}<br><br>", unsafe_allow_html=True
                )
                ip_counter += 1

st.title("Attacker-Server graph")

if st.button("Refresh", key="refresh_button"):
    st.rerun()

data = load_data()

if data is not None:
    if ATTACKER_FIELD in data.columns and SERVER_FIELD in data.columns:
        plot_network_graph(data)
else:
    st.warning("No CSV files found in ./csv. Please add a file.")
