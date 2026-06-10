import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from graph import Graph, Dijkstra, Kruskal

# ── Ma'lumotlar ────────────────────────────────────────
g = Graph()
for shahar in ["Tashkent", "Dubai", "Istanbul", "London"]:
    g.add_airport(shahar)
for src, dst, narx in [
    ("Tashkent", "Dubai",    500),
    ("Tashkent", "Istanbul", 400),
    ("Dubai",    "London",   700),
    ("Istanbul", "London",   600),
]:
    g.add_undirected_flight(src, dst, narx)

d    = Dijkstra()
k    = Kruskal()
dists, prev = d.shortest_path(g.graph, "Tashkent")
mst_edges, mst_total = k.mst(g.graph)

# Dijkstra yo'lini qayta tiklash
def get_path(previous, start, end):
    path, node = [], end
    while node:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path if path[0] == start else []

dijkstra_path = get_path(prev, "Tashkent", "London")
dijkstra_edges = list(zip(dijkstra_path, dijkstra_path[1:]))
mst_edge_set   = {(u, v) for u, v, _ in mst_edges} | {(v, u) for u, v, _ in mst_edges}

# ── NetworkX grafi ─────────────────────────────────────
G = nx.Graph()
edge_weights = {
    ("Tashkent", "Dubai"):    500,
    ("Tashkent", "Istanbul"): 400,
    ("Dubai",    "London"):   700,
    ("Istanbul", "London"):   600,
}
for (u, v), w in edge_weights.items():
    G.add_edge(u, v, weight=w)

pos = {
    "Tashkent": (0.5,  0.85),
    "Dubai":    (0.85, 0.45),
    "Istanbul": (0.15, 0.45),
    "London":   (0.5,  0.08),
}

# ── Rang va qalinlik ────────────────────────────────────
node_colors = {
    "Tashkent": "#EF9F27",   # amber  – start
    "Dubai":    "#D85A30",   # coral
    "Istanbul": "#1D9E75",   # teal
    "London":   "#7F77DD",   # purple – end
}

def edge_style(u, v):
    pair = (u, v)
    rev  = (v, u)
    in_dijk = pair in dijkstra_edges or rev in dijkstra_edges
    in_mst  = pair in mst_edge_set
    if in_dijk and in_mst:
        return "#378ADD", 4.5, "-"      # ko'k + qalin = ikkalasida
    if in_dijk:
        return "#378ADD", 4.5, "-"
    if in_mst:
        return "#1D9E75", 3.0, "-"
    return "#BBBBBB", 1.2, "--"

# ── Rasm ───────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#1a1a2e")

titles = [
    "Dijkstra – Eng qisqa yo'l\nTashkent → London  ($1000)",
    "Kruskal – Minimum Spanning Tree\nUmumiy narx: $1500",
]

for ax, title in zip(axes, titles):
    ax.set_facecolor("#16213e")
    ax.set_title(title, color="white", fontsize=12, pad=14, fontweight="bold")
    ax.axis("off")

    # Barcha edgelar
    for (u, v), w in edge_weights.items():
        color, width, style = edge_style(u, v)
        if ax == axes[1]:           # MST panel uchun qayta hisoblash
            in_mst   = (u, v) in mst_edge_set
            in_dijk  = (u, v) in dijkstra_edges or (v, u) in dijkstra_edges
            if in_mst:
                color, width, style = "#1D9E75", 3.5, "-"
            else:
                color, width, style = "#444444", 1.0, "--"
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v)], ax=ax,
            edge_color=color, width=width, style=style, alpha=0.9
        )

    # Dijkstra panelida path edge larni ustiga qayta chiz
    if ax == axes[0]:
        for u, v in dijkstra_edges:
            nx.draw_networkx_edges(
                G, pos, edgelist=[(u, v)], ax=ax,
                edge_color="#378ADD", width=4.5, style="-",
                arrows=True, arrowsize=25,
                connectionstyle="arc3,rad=0.0"
            )

    # MST panelida MST edge larni ustiga qayta chiz
    if ax == axes[1]:
        for u, v, _ in mst_edges:
            nx.draw_networkx_edges(
                G, pos, edgelist=[(u, v)], ax=ax,
                edge_color="#1D9E75", width=3.5, style="-"
            )

    # Tugunlar
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=[node_colors[n] for n in G.nodes()],
        node_size=2000, alpha=0.95
    )

    # Tugun nomlari + narxlar
    labels_dist = {
        "Tashkent": f"Tashkent\n$0",
        "Dubai":    f"Dubai\n${dists['Dubai']}",
        "Istanbul": f"Istanbul\n${dists['Istanbul']}",
        "London":   f"London\n${dists['London']} ★",
    }
    labels_plain = {n: n for n in G.nodes()}

    nx.draw_networkx_labels(
        G, pos, ax=ax,
        labels=labels_dist if ax == axes[0] else labels_plain,
        font_color="white", font_size=9, font_weight="bold"
    )

    # Edge narxlari
    edge_labels = {(u, v): f"${w}" for (u, v), w in edge_weights.items()}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, ax=ax,
        font_color="#CCCCCC", font_size=9,
        bbox=dict(boxstyle="round,pad=0.2", fc="#16213e", ec="none", alpha=0.7)
    )

# ── Legend ─────────────────────────────────────────────
legend_items = [
    mpatches.Patch(color="#378ADD", label="Dijkstra yo'li"),
    mpatches.Patch(color="#1D9E75", label="MST (Kruskal)"),
    mpatches.Patch(color="#BBBBBB", label="Ishlatilmagan edge"),
    mpatches.Patch(color="#EF9F27", label="Tashkent (start)"),
    mpatches.Patch(color="#7F77DD", label="London (manzil)"),
]
fig.legend(
    handles=legend_items,
    loc="lower center", ncol=5,
    framealpha=0.15, labelcolor="white",
    fontsize=9, facecolor="#1a1a2e",
    bbox_to_anchor=(0.5, -0.02)
)

plt.suptitle("SkyNet – Graf Vizualizatsiyasi", color="white",
             fontsize=15, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("skynet_graph.png", dpi=180, bbox_inches="tight",
            facecolor="#1a1a2e")
print("Saqlandi: skynet_graph.png")