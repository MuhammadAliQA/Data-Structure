import heapq


class Graph:
    def __init__(self):
        self.graph = {}

    def add_airport(self, airport):
        if airport not in self.graph:
            self.graph[airport] = []

    def add_flight(self, source, destination, cost):
        # agar aeroport yo‘q bo‘lsa qo‘shib yuboramiz
        if source not in self.graph:
            self.graph[source] = []
        if destination not in self.graph:
            self.graph[destination] = []

        # ikki tomonlama yo‘l (MST uchun muhim)
        self.graph[source].append((destination, cost))
        self.graph[destination].append((source, cost))

    def display(self):
        print("\n=== REYS TARMOQLARI ===")
        for airport in self.graph:
            print(airport, "->", self.graph[airport])


class Dijkstra:
    def shortest_path(self, graph, start):

        if not graph:
            return "Graf bo'sh"

        if start not in graph:
            return "Aeroport topilmadi"

        distances = {node: float('inf') for node in graph}
        distances[start] = 0

        pq = [(0, start)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in graph[current_node]:
                new_distance = current_distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))

        return distances


class Kruskal:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, nodes):
        for n in nodes:
            self.parent[n] = n
            self.rank[n] = 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        rootA = self.find(a)
        rootB = self.find(b)

        if rootA != rootB:
            if self.rank[rootA] < self.rank[rootB]:
                self.parent[rootA] = rootB
            elif self.rank[rootA] > self.rank[rootB]:
                self.parent[rootB] = rootA
            else:
                self.parent[rootB] = rootA
                self.rank[rootA] += 1

    def mst(self, graph):

        edges = []
        nodes = list(graph.keys())

        for u in graph:
            for v, w in graph[u]:
                edges.append((w, u, v))

        edges.sort()

        self.make_set(nodes)

        mst = []
        total = 0

        for w, u, v in edges:
            if self.find(u) != self.find(v):
                self.union(u, v)
                mst.append((u, v, w))
                total += w

        return mst, total