class RouteFinder:
    """
    Recursive Backtracking – barcha mumkin yo'llarni topadi.
    Aeroport yopilganda muqobil marshrut izlash uchun.

    Murakkablik: O(V!) eng yomon holat (V = tugunlar soni).
    """

    def find(self, graph, start, end, blocked=None):
        """
        graph   – adjacency list
        start   – boshlanish aeroporti
        end     – manzil aeroporti
        blocked – yopiq aeroport nomi (ixtiyoriy)
        """
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
                path.pop()                  # backtrack