import heapq


class Graph:
    """Adjacency List asosida yo'naltirilgan graf (directed graph)."""

    def __init__(self):
        self.graph = {}

    def add_airport(self, airport):
        if airport not in self.graph:
            self.graph[airport] = []

    def add_flight(self, source, destination, cost):
        """Bir tomonlama flight qo'shadi (directed)."""
        if source not in self.graph:
            self.graph[source] = []
        if destination not in self.graph:
            self.graph[destination] = []
        self.graph[source].append((destination, cost))

    def add_undirected_flight(self, source, destination, cost):
        """MST uchun ikki tomonlama flight qo'shadi."""
        self.add_flight(source, destination, cost)
        self.add_flight(destination, source, cost)

    def display(self):
        print("\n" + "=" * 50)
        print("  ✈  SKYNET REYS TARMOQLARI (Flight Network)")
        print("=" * 50)
        for airport, flights in self.graph.items():
            if flights:
                routes = ", ".join(f"{dest} (${cost})" for dest, cost in flights)
                print(f"  {airport:12} -->  {routes}")
            else:
                print(f"  {airport:12} -->  (reyslar yo'q)")
        print("=" * 50)


# ─────────────────────────────────────────────────────
class Dijkstra:
    """Dijkstra algoritmi – eng qisqa yo'lni topadi."""

    def shortest_path(self, graph, start):
        if not graph:
            return None, "Xato: Graf bo'sh!"
        if start not in graph:
            return None, f"Xato: '{start}' aeroport topilmadi!"

        distances = {node: float('inf') for node in graph}
        previous  = {node: None for node in graph}
        distances[start] = 0
        pq = [(0, start)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)
            if current_dist > distances[current_node]:
                continue
            for neighbor, weight in graph[current_node]:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor]  = current_node
                    heapq.heappush(pq, (new_dist, neighbor))

        return distances, previous

    def get_path(self, previous, start, end):
        """previous dict dan yo'lni qayta tiklaydi."""
        path = []
        node = end
        while node is not None:
            path.append(node)
            node = previous[node]
        path.reverse()
        if path[0] != start:
            return []
        return path


# ─────────────────────────────────────────────────────
class Kruskal:
    """Kruskal algoritmi – Minimum Spanning Tree (MST)."""

    def __init__(self):
        self.parent = {}
        self.rank   = {}

    def _make_set(self, nodes):
        for n in nodes:
            self.parent[n] = n
            self.rank[n]   = 0

    def _find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self._find(self.parent[x])   # path compression
        return self.parent[x]

    def _union(self, a, b):
        ra, rb = self._find(a), self._find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True

    def mst(self, graph):
        """MST edgelarini va umumiy narxni qaytaradi."""
        edges = []
        for u in graph:
            for v, w in graph[u]:
                if (w, v, u) not in edges:          # takrorlanishni oldini olish
                    edges.append((w, u, v))
        edges.sort()

        self._make_set(list(graph.keys()))
        result, total = [], 0

        for w, u, v in edges:
            if self._union(u, v):
                result.append((u, v, w))
                total += w

        return result, total