import heapq


class Graph:
    def __init__(self):
        self.graph = {}

    def add_airport(self, airport):
        if airport not in self.graph:
            self.graph[airport] = []

    def add_flight(self, source, destination, cost):
        if source not in self.graph:
            self.graph[source] = []
        if destination not in self.graph:
            self.graph[destination] = []
        self.graph[source].append((destination, cost))

    def add_undirected_flight(self, source, destination, cost):
        self.add_flight(source, destination, cost)
        self.add_flight(destination, source, cost)

    def display(self):
        print("\n" + "=" * 50)
        print("  REYS TARMOQLARI")
        print("=" * 50)
        for airport, flights in self.graph.items():
            if flights:
                routes = ", ".join(f"{dest} (${cost})" for dest, cost in flights)
                print(f"  {airport:12} -->  {routes}")
            else:
                print(f"  {airport:12} -->  (reyslar yo'q)")
        print("=" * 50)


class Dijkstra:
    def shortest_path(self, graph, start):
        if not graph:
            return None, "Xato: Graf bo'sh!"
        if start not in graph:
            return None, f"Xato: '{start}' topilmadi!"

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
        path = []
        node = end
        while node is not None:
            path.append(node)
            node = previous[node]
        path.reverse()
        if not path or path[0] != start:
            return []
        return path


class Kruskal:
    def __init__(self):
        self.parent = {}
        self.rank   = {}

    def _make_set(self, nodes):
        for n in nodes:
            self.parent[n] = n
            self.rank[n]   = 0

    def _find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self._find(self.parent[x])
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
        edges = []
        for u in graph:
            for v, w in graph[u]:
                if (w, v, u) not in edges:
                    edges.append((w, u, v))
        edges.sort()
        self._make_set(list(graph.keys()))
        result, total = [], 0
        for w, u, v in edges:
            if self._union(u, v):
                result.append((u, v, w))
                total += w
        return result, total


class BellmanFord:
    def shortest_path(self, graph, start):
        if not graph:
            return None, "Xato: Graf bo'sh!"
        if start not in graph:
            return None, f"Xato: '{start}' topilmadi!"

        nodes     = list(graph.keys())
        distances = {n: float('inf') for n in nodes}
        previous  = {n: None for n in nodes}
        distances[start] = 0

        for _ in range(len(nodes) - 1):
            updated = False
            for u in graph:
                if distances[u] == float('inf'):
                    continue
                for v, w in graph[u]:
                    if distances[u] + w < distances[v]:
                        distances[v] = distances[u] + w
                        previous[v]  = u
                        updated = True
            if not updated:
                break

        for u in graph:
            for v, w in graph[u]:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    return None, "Xato: Manfiy sikl aniqlandi!"

        return distances, previous

    def get_path(self, previous, start, end):
        if previous.get(end) is None and end != start:
            return []
        path, node = [], end
        while node is not None:
            path.append(node)
            node = previous[node]
        path.reverse()
        return path if path[0] == start else []


class Prim:
    def mst(self, graph, start=None):
        if not graph:
            return [], 0
        if start is None:
            start = next(iter(graph))

        visited = {start}
        heap = [(w, start, v) for v, w in graph[start]]
        heapq.heapify(heap)
        result, total = [], 0

        while heap and len(visited) < len(graph):
            w, u, v = heapq.heappop(heap)
            if v in visited:
                continue
            visited.add(v)
            result.append((u, v, w))
            total += w
            for neighbor, weight in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(heap, (weight, v, neighbor))

        return result, total