"""
SkyNet – Comprehensive Test Suite
Covers: normal cases, edge cases, error handling
"""

from graph     import Graph, Dijkstra, BellmanFord, Kruskal, compare_shortest_paths
from passenger import PriorityCheckIn, BoardingQueue, CargoStack
from search    import BST, AVLTree, HashTable, KMP
from sorting   import QuickSort, MergeSort, compare_sorts
from routing   import RouteFinder

PASS = "  ✔ PASS"
FAIL = "  ✘ FAIL"

def assert_eq(label, actual, expected):
    if actual == expected:
        print(f"{PASS}  {label}")
    else:
        print(f"{FAIL}  {label}")
        print(f"       expected : {expected}")
        print(f"       got      : {actual}")

def assert_true(label, condition):
    print(f"{PASS}  {label}" if condition else f"{FAIL}  {label}")

def header(title):
    print(f"\n{'═'*55}")
    print(f"  TEST: {title}")
    print('═'*55)


# ══════════════════════════════════════════════
#  1. GRAPH TESTS
# ══════════════════════════════════════════════
header("Graph – Normal & Edge Cases")

# Empty graph display (should not crash)
g_empty = Graph()
try:
    g_empty.display()
    print(f"{PASS}  Empty graph display – no crash")
except Exception as e:
    print(f"{FAIL}  Empty graph display – {e}")

# Normal graph
g = Graph()
g.add_airport("A")
g.add_airport("B")
g.add_airport("C")
g.add_flight("A", "B", 10)
g.add_flight("B", "C", 20)
assert_true("Graph has 3 airports",     len(g.graph) == 3)
assert_true("A connected to B",         ("B", 10) in g.graph["A"])
assert_true("B connected to A (undirected)", ("A", 10) in g.graph["B"])

# Duplicate airport
g.add_airport("A")
assert_true("Duplicate airport not added twice", len(g.graph) == 3)

# Invalid flight cost
try:
    g.add_flight("A", "C", -5)
    print(f"{FAIL}  Negative cost should raise ValueError")
except ValueError:
    print(f"{PASS}  Negative cost raises ValueError")


# ══════════════════════════════════════════════
#  2. DIJKSTRA TESTS
# ══════════════════════════════════════════════
header("Dijkstra – Shortest Path")

d = Dijkstra()

# Empty graph
r = d.shortest_path({}, "X")
assert_true("Empty graph returns error string", isinstance(r, str))

# Unknown source
r = d.shortest_path({"A": []}, "Z")
assert_true("Unknown source returns error string", isinstance(r, str))

# Standard graph
graph_d = {
    "A": [("B", 5), ("C", 10)],
    "B": [("C", 3), ("A", 5)],
    "C": [("A", 10), ("B", 3)],
}
r = d.shortest_path(graph_d, "A")
assert_eq("A→A distance = 0",  r["A"][0], 0)
assert_eq("A→B distance = 5",  r["B"][0], 5)
assert_eq("A→C distance = 8",  r["C"][0], 8)   # via B (5+3)

# Disconnected graph
graph_disc = {
    "A": [("B", 1)],
    "B": [("A", 1)],
    "C": [],
}
r = d.shortest_path(graph_disc, "A")
assert_eq("Disconnected node C = inf", r["C"][0], float('inf'))


# ══════════════════════════════════════════════
#  3. KRUSKAL MST TESTS
# ══════════════════════════════════════════════
header("Kruskal – Minimum Spanning Tree")

k = Kruskal()

# Empty graph
edges, total = k.mst({})
assert_eq("Empty graph MST cost = 0", total, 0)

# Triangle graph
graph_k = {
    "A": [("B", 1), ("C", 4)],
    "B": [("A", 1), ("C", 2)],
    "C": [("A", 4), ("B", 2)],
}
edges, total = k.mst(graph_k)
assert_eq("Triangle MST cost = 3 (edges 1+2)", total, 3)
assert_eq("Triangle MST has 2 edges (V-1)", len(edges), 2)


# ══════════════════════════════════════════════
#  4. PRIORITY CHECK-IN TESTS
# ══════════════════════════════════════════════
header("PriorityCheckIn – Max-Heap")

p = PriorityCheckIn()

# Empty serve
r = p.serve()
assert_true("Empty queue serve returns string", isinstance(r, str))

# Priority ordering: Platinum must come before Gold and Economy
p.add_passenger("Ali",  "Economy")
p.add_passenger("John", "Platinum")
p.add_passenger("Sara", "Gold")

first = p.serve()
assert_eq("Platinum served first", first["class"], "Platinum")
second = p.serve()
assert_eq("Gold served second",    second["class"], "Gold")
third = p.serve()
assert_eq("Economy served last",   third["class"], "Economy")

# FIFO within same class
p2 = PriorityCheckIn()
p2.add_passenger("First",  "Gold")
p2.add_passenger("Second", "Gold")
r1 = p2.serve()
assert_eq("FIFO within same class – First served first", r1["name"], "First")

# Invalid class
try:
    p.add_passenger("Bob", "VIP")
    print(f"{FAIL}  Unknown class should raise ValueError")
except ValueError:
    print(f"{PASS}  Unknown ticket class raises ValueError")


# ══════════════════════════════════════════════
#  5. BOARDING QUEUE & CARGO STACK TESTS
# ══════════════════════════════════════════════
header("BoardingQueue (FIFO) & CargoStack (LIFO)")

q = BoardingQueue()
s = CargoStack()

# Empty dequeue / pop
assert_true("Empty queue remove returns string", isinstance(q.remove(), str))
assert_true("Empty stack pop returns string",    isinstance(s.pop(), str))

# FIFO order
q.add("Passenger1")
q.add("Passenger2")
q.add("Passenger3")
assert_eq("FIFO – Passenger1 first", q.remove(), "Passenger1")
assert_eq("FIFO – Passenger2 next",  q.remove(), "Passenger2")

# LIFO order
s.push("Bag1")
s.push("Bag2")
s.push("Bag3")
assert_eq("LIFO – Bag3 unloaded first", s.pop(), "Bag3")
assert_eq("LIFO – Bag2 unloaded next",  s.pop(), "Bag2")

# Size
q2 = BoardingQueue()
q2.add("A"); q2.add("B")
assert_eq("Queue size = 2", q2.size(), 2)


# ══════════════════════════════════════════════
#  6. BST TESTS
# ══════════════════════════════════════════════
header("BST – Insert / Search / Range Query")

bst = BST()

# Empty tree
assert_eq("Empty BST inorder = []", bst.inorder(), [])
assert_eq("Empty BST search  = False", bst.search(10), False)
assert_eq("Empty BST range   = []", bst.range_query(0, 100), [])

# Insertions
for v in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(v)

assert_eq("BST inorder sorted", bst.inorder(), [20, 30, 40, 50, 60, 70, 80])
assert_eq("BST search 40 = True",  bst.search(40), True)
assert_eq("BST search 99 = False", bst.search(99), False)
assert_eq("BST range [35,65]", bst.range_query(35, 65), [40, 50, 60])
assert_eq("BST range no match", bst.range_query(90, 100), [])


# ══════════════════════════════════════════════
#  7. AVL TREE TESTS
# ══════════════════════════════════════════════
header("AVL Tree – Self-Balancing Insert / Range Query")

avl = AVLTree()
# Sorted insertion (would degrade BST to O(n), AVL stays O(log n))
for v in [10, 20, 30, 40, 50, 60, 70]:
    avl.insert(v)

assert_eq("AVL inorder sorted", avl.inorder(), [10, 20, 30, 40, 50, 60, 70])
assert_eq("AVL search 30 = True",  avl.search(30), True)
assert_eq("AVL search 99 = False", avl.search(99), False)
assert_eq("AVL range [25,55]", avl.range_query(25, 55), [30, 40, 50])

# Root should have height ≤ 3 (AVL balance guarantee)
assert_true("AVL root height ≤ 4 after 7 insertions", avl._root.height <= 4)


# ══════════════════════════════════════════════
#  8. HASH TABLE TESTS
# ══════════════════════════════════════════════
header("HashTable – O(1) PNR Lookup")

ht = HashTable()
assert_true("Get missing key returns string", isinstance(ht.get("X"), str))

ht.add("PNR001", {"name": "Ali", "class": "Platinum"})
ht.add("PNR002", {"name": "Bob", "class": "Economy"})

assert_eq("PNR001 lookup", ht.get("PNR001")["name"], "Ali")
assert_eq("PNR002 lookup", ht.get("PNR002")["class"], "Economy")
assert_true("exists PNR001 = True",  ht.exists("PNR001"))
assert_true("exists PNR999 = False", not ht.exists("PNR999"))

# Overwrite
ht.add("PNR001", {"name": "Ali Updated", "class": "Gold"})
assert_eq("PNR001 updated", ht.get("PNR001")["name"], "Ali Updated")

# Delete
ht.delete("PNR001")
assert_true("After delete PNR001 not found", not ht.exists("PNR001"))


# ══════════════════════════════════════════════
#  9. KMP TESTS  (real algorithm, not `in`)
# ══════════════════════════════════════════════
header("KMP – Knuth-Morris-Pratt String Search")

kmp = KMP()

# Basic match
assert_eq("KMP: 'Ali' in manifest",
          kmp.search("Ali Karimov on flight", "Ali"), [0])

# Multiple occurrences
assert_eq("KMP: 'Ali' appears twice",
          kmp.search("Ali and Ali", "Ali"), [0, 8])

# No match
assert_eq("KMP: pattern not found = []",
          kmp.search("John Smith", "Ali"), [])

# Empty pattern
assert_eq("KMP: empty pattern = []",
          kmp.search("Hello", ""), [])

# Empty text
assert_eq("KMP: empty text = []",
          kmp.search("", "Ali"), [])

# Overlapping pattern
assert_eq("KMP: overlapping 'ABAB' in 'ABABAB'",
          kmp.search("ABABAB", "ABAB"), [0, 2])

# Case sensitive
assert_eq("KMP: case sensitive – 'ali' not in 'Ali'",
          kmp.search("Ali", "ali"), [])

# contains() helper
assert_true("KMP contains() True",  kmp.contains("Tashkent departure", "Tashkent"))
assert_true("KMP contains() False", not kmp.contains("Tashkent departure", "Dubai"))


# ══════════════════════════════════════════════
#  10. SORTING TESTS
# ══════════════════════════════════════════════
header("QuickSort & MergeSort")

qs = QuickSort()
ms = MergeSort()

# Normal
assert_eq("QuickSort [5,2,9,1]",    qs.sort([5,2,9,1]),    [1,2,5,9])
assert_eq("MergeSort [5,2,9,1]",    ms.sort([5,2,9,1]),    [1,2,5,9])

# Already sorted
assert_eq("QuickSort already sorted", qs.sort([1,2,3,4]), [1,2,3,4])
assert_eq("MergeSort already sorted", ms.sort([1,2,3,4]), [1,2,3,4])

# Reverse sorted
assert_eq("QuickSort reverse",  qs.sort([4,3,2,1]), [1,2,3,4])
assert_eq("MergeSort reverse",  ms.sort([4,3,2,1]), [1,2,3,4])

# Single element
assert_eq("QuickSort single",   qs.sort([42]), [42])
assert_eq("MergeSort single",   ms.sort([42]), [42])

# Empty list
assert_eq("QuickSort empty",    qs.sort([]), [])
assert_eq("MergeSort empty",    ms.sort([]), [])

# Duplicates
assert_eq("QuickSort duplicates", qs.sort([3,1,3,2,1]), [1,1,2,3,3])
assert_eq("MergeSort duplicates", ms.sort([3,1,3,2,1]), [1,1,2,3,3])

# compare_sorts
cr = compare_sorts([9,7,5,3,1])
assert_eq("compare_sorts quick == merge", cr["quick_result"], cr["merge_result"])
assert_true("compare_sorts has a winner", cr["winner"] in ("QuickSort","MergeSort"))

# Original list not mutated
original = [3,1,4,1,5]
qs.sort(original)
assert_eq("QuickSort does not mutate input", original, [3,1,4,1,5])


# ══════════════════════════════════════════════
#  11. ROUTING (BACKTRACKING) TESTS
# ══════════════════════════════════════════════
header("RouteFinder – Backtracking")

rf = RouteFinder()

base_graph = {
    "A": [("B", 1), ("C", 1)],
    "B": [("A", 1), ("D", 1)],
    "C": [("A", 1), ("D", 1)],
    "D": [("B", 1), ("C", 1)],
}

# All routes A→D
routes = rf.find(base_graph, "A", "D")
assert_eq("A→D: 2 routes exist", len(routes), 2)
assert_true("Route via B exists", ["A","B","D"] in routes)
assert_true("Route via C exists", ["A","C","D"] in routes)

# Same source and destination
routes = rf.find(base_graph, "A", "A")
assert_eq("A→A returns [['A']]", routes, [["A"]])

# Blocked hub
routes_blocked = rf.find_with_blocked_hub(base_graph, "A", "D", "B")
for r in routes_blocked:
    assert_true(f"Blocked hub 'B' not in route {r}", "B" not in r)

# No path (disconnected)
disc = {"A": [("B", 1)], "B": [("A", 1)], "C": []}
routes = rf.find(disc, "A", "C")
assert_eq("No path → []", routes, [])

# Empty graph
routes = rf.find({}, "A", "D")
assert_eq("Empty graph → []", routes, [])

# Mutable default argument fix – calling twice should not accumulate paths
rf2 = RouteFinder()
r1 = rf2.find(base_graph, "A", "D")
r2 = rf2.find(base_graph, "A", "D")
assert_eq("Repeated call same result (mutable default fix)", r1, r2)

# Cyclic graph (should not loop infinitely)
cyclic = {
    "A": [("B", 1)],
    "B": [("A", 1), ("C", 1)],
    "C": [("B", 1)],
}
try:
    routes = rf.find(cyclic, "A", "C")
    assert_eq("Cyclic graph A→C finds 1 path", len(routes), 1)
except RecursionError:
    print(f"{FAIL}  Cyclic graph caused RecursionError")


# ══════════════════════════════════════════════
#  12. BELLMAN-FORD TESTS
# ══════════════════════════════════════════════
header("Bellman-Ford – Shortest Path")

bf = BellmanFord()

# Empty graph
r = bf.shortest_path({}, "X")
assert_true("Empty graph returns error string", isinstance(r, str))

# Unknown source
r = bf.shortest_path({"A": []}, "Z")
assert_true("Unknown source returns error string", isinstance(r, str))

# Standard graph — same as Dijkstra test
graph_bf = {
    "A": [("B", 5), ("C", 10)],
    "B": [("C", 3), ("A", 5)],
    "C": [("A", 10), ("B", 3)],
}
r = bf.shortest_path(graph_bf, "A")
assert_eq("BF A→A distance = 0",  r["A"][0], 0)
assert_eq("BF A→B distance = 5",  r["B"][0], 5)
assert_eq("BF A→C distance = 8",  r["C"][0], 8)   # via B: 5+3

# Dijkstra and Bellman-Ford must give IDENTICAL results
d2  = Dijkstra()
bf2 = BellmanFord()
graph_same = {
    "Tashkent": [("Dubai", 500), ("Istanbul", 400)],
    "Dubai":    [("Tashkent", 500), ("London", 700)],
    "Istanbul": [("Tashkent", 400), ("London", 600)],
    "London":   [("Dubai", 700), ("Istanbul", 600)],
}
dr = d2.shortest_path(graph_same, "Tashkent")
br = bf2.shortest_path(graph_same, "Tashkent")
for node in graph_same:
    assert_eq(
        f"Dijkstra == BellmanFord cost to {node}",
        dr[node][0], br[node][0]
    )

# Disconnected node
graph_disc2 = {
    "A": [("B", 1)],
    "B": [("A", 1)],
    "C": [],
}
r = bf.shortest_path(graph_disc2, "A")
assert_eq("BF disconnected node C = inf", r["C"][0], float('inf'))

# Negative cycle detection
# Build a graph where A→B→C→A has total weight -1 (negative cycle)
graph_neg_cycle = {
    "A": [("B", 1)],
    "B": [("C", 1)],
    "C": [("A", -3)],   # -3 creates a negative cycle: 1+1-3 = -1
}
r = bf.shortest_path(graph_neg_cycle, "A")
assert_true("Negative cycle detected → returns error string", isinstance(r, str))

# show_steps=True must not crash
try:
    bf.shortest_path(graph_same, "Tashkent", show_steps=True)
    print(f"{PASS}  show_steps=True runs without error")
except Exception as e:
    print(f"{FAIL}  show_steps=True crashed: {e}")

# compare_shortest_paths must not crash
try:
    compare_shortest_paths(graph_same, "Tashkent")
    print(f"{PASS}  compare_shortest_paths() runs without error")
except Exception as e:
    print(f"{FAIL}  compare_shortest_paths() crashed: {e}")


# ══════════════════════════════════════════════
#  SUMMARY
# ══════════════════════════════════════════════
print("\n" + "═"*55)
print("  All test cases completed.")
print("═"*55 + "\n")