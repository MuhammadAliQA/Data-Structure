class RouteFinder:
    def find(self, graph, start, end, path=[]):

        path = path + [start]

        if start == end:
            return [path]

        if start not in graph:
            return []

        routes = []

        for n, _ in graph[start]:
            if n not in path:
                new_routes = self.find(graph, n, end, path)
                for r in new_routes:
                    routes.append(r)

        return routes