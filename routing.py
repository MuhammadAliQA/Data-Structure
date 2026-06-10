class RouteFinder:
    def find(self, graph, start, end, blocked=None):
        if blocked is None:
            blocked = set()
        else:
            blocked = {blocked}
        all_paths = []
        self._backtrack(graph, start, end, blocked, [start], all_paths)
        return all_paths

    def _backtrack(self, graph, current, end, blocked, path, all_paths):
        if current == end:
            all_paths.append(path[:])
            return
        if current not in graph:
            return
        for neighbor, _ in graph[current]:
            if neighbor not in path and neighbor not in blocked:
                path.append(neighbor)
                self._backtrack(graph, neighbor, end, blocked, path, all_paths)
                path.pop()