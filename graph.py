import heapq


# ══════════════════════════════════════════════
#  GRAPH  –  Adjacency List representation
# ══════════════════════════════════════════════
class Graph:
    """
    ADT: Graph
    Nodes  = airports (strings)
    Edges  = direct flights with a numeric cost/weight

    Operations
    ----------
    add_airport(name)            -> None
    add_flight(src, dst, cost)   -> None   (undirected for MST; directed for Dijkstra)
    display()                    -> None
    """

    def __init__(self):
        self._graph = {}          # { airport: [(neighbour, cost), ...] }

    # ---------- public interface ----------

    @property
    def graph(self):
        return self._graph

    def add_airport(self, airport: str) -> None:
        if not isinstance(airport, str) or not airport.strip():
            raise ValueError("Airport name must be a non-empty string.")
        if airport not in self._graph:
            self._graph[airport] = []

    def add_flight(self, source: str, destination: str, cost: float) -> None:
        if cost < 0:
            raise ValueError("Flight cost cannot be negative.")
        # Auto-create nodes if they don't exist
        for node in (source, destination):
            if node not in self._graph:
                self._graph[node] = []
        # Undirected (both directions) – needed for MST
        self._graph[source].append((destination, cost))
        self._graph[destination].append((source, cost))

    def display(self) -> None:
        if not self._graph:
            print("  [Graph is empty – no airports added yet]")
            return
        print("\n  ╔══ FLIGHT NETWORK ══╗")
        for airport, routes in self._graph.items():
            formatted = ", ".join(f"{dst}({cost})" for dst, cost in routes)
            print(f"  ║  {airport:15s} → {formatted if formatted else '(no outgoing flights)'}")
        print("  ╚═══════════════════╝")


# ══════════════════════════════════════════════
#  DIJKSTRA'S ALGORITHM
#  Time:  O((V + E) log V)  using a min-heap
#  Space: O(V)
# ══════════════════════════════════════════════
class Dijkstra:
    """
    Finds the shortest (cheapest) path from a single source to ALL other airports.
    Returns a dict  { airport: (total_cost, path_list) }.
    """

    def shortest_path(self, graph: dict, start: str) -> dict | str:
        # ── Edge-case guards ──
        if not graph:
            return "Error: Flight network is empty."
        if start not in graph:
            return f"Error: Airport '{start}' not found in network."

        dist = {node: float('inf') for node in graph}
        prev = {node: None for node in graph}
        dist[start] = 0

        # min-heap: (distance, node)
        heap = [(0, start)]

        while heap:
            curr_dist, curr_node = heapq.heappop(heap)

            if curr_dist > dist[curr_node]:
                continue                          # stale entry – skip

            for neighbour, weight in graph[curr_node]:
                new_dist = curr_dist + weight
                if new_dist < dist[neighbour]:
                    dist[neighbour] = new_dist
                    prev[neighbour] = curr_node
                    heapq.heappush(heap, (new_dist, neighbour))

        # Reconstruct paths
        result = {}
        for node in graph:
            path = []
            step = node
            while step is not None:
                path.append(step)
                step = prev[step]
            path.reverse()
            result[node] = (dist[node], path if dist[node] != float('inf') else [])

        return result


# ══════════════════════════════════════════════
#  BELLMAN-FORD ALGORITHM
#  Time:  O(V × E)   — slower than Dijkstra
#  Space: O(V)
#  Advantage: handles NEGATIVE weight edges
#             detects NEGATIVE CYCLES
# ══════════════════════════════════════════════
class BellmanFord:
    """
    Bellman-Ford finds shortest paths from a single source.

    Key difference from Dijkstra
    ----------------------------
    Dijkstra uses a greedy min-heap and assumes all weights >= 0.
    Bellman-Ford relaxes EVERY edge (V-1) times, so it works even
    when some flight costs are negative (e.g. subsidised routes)
    and can detect negative-weight cycles.

    Step-by-step (illustration mode)
    ---------------------------------
    Each 'relaxation pass' is printed so the user can see exactly
    how distances shrink iteration by iteration — this satisfies
    the D1 'illustration' requirement.
    """

    def shortest_path(self, graph: dict, start: str,
                      show_steps: bool = False) -> dict | str:
        # ── Edge-case guards ──
        if not graph:
            return "Error: Flight network is empty."
        if start not in graph:
            return f"Error: Airport '{start}' not found in network."

        nodes = list(graph.keys())
        V     = len(nodes)

        dist = {node: float('inf') for node in nodes}
        prev = {node: None         for node in nodes}
        dist[start] = 0

        # Build a flat edge list  [(u, v, w), ...]
        # For undirected graphs each edge appears twice — that is fine;
        # relaxing both directions is correct and harmless.
        edges = []
        for u in graph:
            for v, w in graph[u]:
                edges.append((u, v, w))

        if show_steps:
            print(f"\n  {'─'*48}")
            print(f"  Bellman-Ford step-by-step from '{start}'")
            print(f"  Nodes: {nodes}")
            print(f"  Edges: {len(edges)}   Relaxation passes needed: {V-1}")
            print(f"  {'─'*48}")

        # ── V-1 relaxation passes ──
        for iteration in range(V - 1):
            updated = False
            for u, v, w in edges:
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    updated = True

            if show_steps:
                changed = {n: d for n, d in dist.items() if d != float('inf')}
                print(f"  Pass {iteration+1:>2}: {changed}")

            if not updated:          # early exit – converged
                if show_steps:
                    print(f"  ✔ Converged early at pass {iteration+1}")
                break

        # ── Negative-cycle detection (V-th pass) ──
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                return "Error: Negative-weight cycle detected in flight network."

        # Reconstruct paths
        result = {}
        for node in nodes:
            path = []
            step = node
            while step is not None:
                path.append(step)
                step = prev[step]
            path.reverse()
            result[node] = (dist[node], path if dist[node] != float('inf') else [])

        return result


# ══════════════════════════════════════════════
#  D1 – COMPARISON: Dijkstra vs Bellman-Ford
#  Illustrates both algorithms on the same graph
#  and highlights the differences.
# ══════════════════════════════════════════════
import time as _time

def compare_shortest_paths(graph: dict, start: str) -> None:
    """
    D1 requirement: run BOTH shortest-path algorithms on the same
    flight network, print step-by-step illustrations, then compare:
      • results (must be identical for non-negative weights)
      • execution time
      • Big-O complexity
      • when each algorithm should be preferred
    """
    WIDTH = 52

    def box(text):
        print(f"\n  ╔{'═'*WIDTH}╗")
        for line in text.strip().split('\n'):
            print(f"  ║  {line:<{WIDTH-2}}║")
        print(f"  ╚{'═'*WIDTH}╝")

    box(
        "D1 – Two Shortest Path Algorithms\n"
        "  Dijkstra  vs  Bellman-Ford\n"
        f"  Source airport: {start}"
    )

    # ── Run Dijkstra with timing ──
    print(f"\n  {'━'*WIDTH}")
    print("  ALGORITHM 1 – DIJKSTRA")
    print(f"  {'━'*WIDTH}")
    print("  Strategy : Greedy – always expand the CHEAPEST known node")
    print("  Data str : Min-Heap (Priority Queue)")
    print("  Time     : O((V + E) log V)")
    print("  Handles  : Non-negative weights ONLY")
    print()

    d = Dijkstra()
    t0      = _time.perf_counter()
    d_result = d.shortest_path(graph, start)
    d_time  = (_time.perf_counter() - t0) * 1_000_000

    if isinstance(d_result, str):
        print(f"  {d_result}")
        return

    print(f"  Results from '{start}':")
    for dest, (cost, path) in d_result.items():
        if dest == start:
            continue
        c = str(cost) if cost != float('inf') else "∞"
        p = " → ".join(path) if path else "unreachable"
        print(f"    {dest:<15} cost={c:<8} path: {p}")
    print(f"\n  Time taken: {d_time:.3f} µs")

    # ── Run Bellman-Ford with step-by-step illustration ──
    print(f"\n  {'━'*WIDTH}")
    print("  ALGORITHM 2 – BELLMAN-FORD")
    print(f"  {'━'*WIDTH}")
    print("  Strategy : Relaxation – repeat V-1 times over ALL edges")
    print("  Data str : Simple edge list (no heap needed)")
    print("  Time     : O(V × E)")
    print("  Handles  : Negative weights ✔  |  Detects negative cycles ✔")

    bf = BellmanFord()
    t0      = _time.perf_counter()
    bf_result = bf.shortest_path(graph, start, show_steps=True)
    bf_time = (_time.perf_counter() - t0) * 1_000_000

    if isinstance(bf_result, str):
        print(f"  {bf_result}")
        return

    print(f"\n  Results from '{start}':")
    for dest, (cost, path) in bf_result.items():
        if dest == start:
            continue
        c = str(cost) if cost != float('inf') else "∞"
        p = " → ".join(path) if path else "unreachable"
        print(f"    {dest:<15} cost={c:<8} path: {p}")
    print(f"\n  Time taken: {bf_time:.3f} µs")

    # ── Side-by-side comparison ──
    print(f"\n  {'━'*WIDTH}")
    print("  COMPARISON SUMMARY")
    print(f"  {'━'*WIDTH}")

    # Verify results match
    match = all(
        d_result[n][0] == bf_result[n][0]
        for n in d_result if n in bf_result
    )
    print(f"  Results identical     : {'✔ YES' if match else '✘ NO (check for negative edges)'}")
    print(f"  Dijkstra  time        : {d_time:.3f} µs")
    print(f"  Bellman-Ford time     : {bf_time:.3f} µs")
    faster = "Dijkstra" if d_time <= bf_time else "Bellman-Ford"
    print(f"  Faster on this graph  : ✔ {faster}")

    print(f"""
  ┌─────────────────────────────────────────────────┐
  │           WHEN TO USE WHICH?                    │
  ├──────────────────┬──────────────────────────────┤
  │  DIJKSTRA        │  BELLMAN-FORD                │
  ├──────────────────┼──────────────────────────────┤
  │ All weights ≥ 0  │ Negative weights allowed     │
  │ O((V+E) log V)   │ O(V × E)  — slower           │
  │ Uses min-heap    │ Simple edge list              │
  │ Greedy approach  │ Dynamic programming style    │
  │ No cycle detect  │ Detects negative cycles      │
  │ Best: large maps │ Best: financial/subsidised   │
  │ (Google Maps)    │ route networks               │
  └──────────────────┴──────────────────────────────┘""")


# ══════════════════════════════════════════════
#  KRUSKAL'S ALGORITHM  –  Minimum Spanning Tree
#  Time:  O(E log E)
#  Space: O(V)
# ══════════════════════════════════════════════
class Kruskal:
    """
    Builds the MST of the airport network using Union-Find (disjoint sets).
    Returned value: (list_of_edges, total_cost)
    """

    def __init__(self):
        self._parent = {}
        self._rank   = {}

    # ---------- Union-Find helpers ----------

    def _make_set(self, nodes):
        for n in nodes:
            self._parent[n] = n
            self._rank[n]   = 0

    def _find(self, x):
        if self._parent[x] != x:
            self._parent[x] = self._find(self._parent[x])   # path compression
        return self._parent[x]

    def _union(self, a, b) -> bool:
        rootA, rootB = self._find(a), self._find(b)
        if rootA == rootB:
            return False                                      # already connected
        if self._rank[rootA] < self._rank[rootB]:
            self._parent[rootA] = rootB
        elif self._rank[rootA] > self._rank[rootB]:
            self._parent[rootB] = rootA
        else:
            self._parent[rootB] = rootA
            self._rank[rootA]  += 1
        return True

    # ---------- public ----------

    def mst(self, graph: dict) -> tuple:
        if not graph:
            return [], 0

        # Collect unique edges (avoid duplicates from undirected graph)
        seen_edges = set()
        edges = []
        for u in graph:
            for v, w in graph[u]:
                key = tuple(sorted([u, v])) + (w,)
                if key not in seen_edges:
                    seen_edges.add(key)
                    edges.append((w, u, v))

        edges.sort()
        self._make_set(list(graph.keys()))

        mst_edges = []
        total_cost = 0

        for w, u, v in edges:
            if self._union(u, v):
                mst_edges.append((u, v, w))
                total_cost += w

        return mst_edges, total_cost