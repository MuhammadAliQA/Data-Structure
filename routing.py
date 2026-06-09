# ══════════════════════════════════════════════
#  ROUTE FINDER  –  Recursive Backtracking
#  Finds ALL possible alternative paths between
#  two airports when the primary hub is blocked.
#
#  Time  : O(V!)  worst case (all permutations)
#  Space : O(V)   recursion stack depth
# ══════════════════════════════════════════════
class RouteFinder:
    """
    Uses recursive backtracking to explore every possible flight path
    between a source and destination.

    A 'blocked' set can be passed to simulate airspace closures or
    hub unavailability – those airports will be skipped entirely.

    FIX applied: the original code used `path=[]` as a default mutable
    argument, which caused paths from previous calls to persist across
    invocations.  The fix uses `path=None` and initialises inside the
    function body.
    """

    def find(
        self,
        graph:   dict,
        start:   str,
        end:     str,
        path:    list  = None,   # ← FIX: was `path=[]` (mutable default bug)
        blocked: set   = None,
    ) -> list:
        """
        Return a list of all valid routes from `start` to `end`.
        Each route is itself a list of airport names.

        Parameters
        ----------
        graph   : adjacency dict  { airport: [(neighbour, cost), ...] }
        start   : origin airport
        end     : destination airport
        path    : airports already visited on this branch (internal use)
        blocked : set of airports to treat as unavailable (e.g. closed hub)

        Example
        -------
        rf = RouteFinder()
        routes = rf.find(graph, "Tashkent", "London", blocked={"Dubai"})
        """
        # ── Initialise on first call ──
        if path is None:
            path = []
        if blocked is None:
            blocked = set()

        # ── Edge-case guards ──
        if not graph:
            return []
        if start not in graph or end not in graph:
            return []

        path = path + [start]          # create a NEW list each time (no mutation)

        # Base case – reached destination
        if start == end:
            return [path]

        routes = []

        for neighbour, _ in graph[start]:
            # Skip visited nodes (cycle prevention) and blocked airports
            if neighbour in path or neighbour in blocked:
                continue
            new_routes = self.find(graph, neighbour, end, path, blocked)
            routes.extend(new_routes)

        return routes

    def find_with_blocked_hub(
        self,
        graph:       dict,
        start:       str,
        end:         str,
        blocked_hub: str,
    ) -> list:
        """
        Convenience wrapper: find all paths while treating `blocked_hub`
        as an unavailable airport.
        """
        return self.find(graph, start, end, blocked=({blocked_hub}))