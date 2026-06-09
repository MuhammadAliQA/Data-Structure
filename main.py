from graph     import Graph, Dijkstra, BellmanFord, Kruskal, compare_shortest_paths
from passenger import PriorityCheckIn, BoardingQueue, CargoStack
from search    import BST, AVLTree, HashTable, KMP
from sorting   import compare_sorts
from routing   import RouteFinder

# ══════════════════════════════════════════════
#  SKYNET – Global Aviation Logistics System
#  Console Application  (main entry point)
# ══════════════════════════════════════════════

# ── Global instances ──────────────────────────
graph    = Graph()
dijkstra = Dijkstra()
bellman  = BellmanFord()
kruskal  = Kruskal()

check_in = PriorityCheckIn()
boarding = BoardingQueue()
cargo    = CargoStack()

bst      = BST()
avl      = AVLTree()
hash_tbl = HashTable()
kmp      = KMP()

router   = RouteFinder()


# ──────────────────────────────────────────────
def setup():
    """Seed the system with initial airport and price data."""
    for airport in ["Tashkent", "Dubai", "Istanbul", "London", "Moscow", "Delhi"]:
        graph.add_airport(airport)

    flights = [
        ("Tashkent", "Dubai",    500),
        ("Tashkent", "Istanbul", 400),
        ("Tashkent", "Moscow",   300),
        ("Dubai",    "London",   700),
        ("Dubai",    "Delhi",    350),
        ("Istanbul", "London",   600),
        ("Moscow",   "Istanbul", 450),
        ("Delhi",    "London",   800),
    ]
    for src, dst, cost in flights:
        graph.add_flight(src, dst, cost)

    for price in [350, 500, 700, 400, 300, 800, 600, 450]:
        bst.insert(price)
        avl.insert(price)

    hash_tbl.add("PNR001", {"name": "Ali Karimov",  "seat": "1A",  "class": "Platinum"})
    hash_tbl.add("PNR002", {"name": "John Smith",   "seat": "12B", "class": "Gold"})
    hash_tbl.add("PNR003", {"name": "Sara Johnson", "seat": "23C", "class": "Economy"})


# ──────────────────────────────────────────────
def sep(title=""):
    line = "─" * 50
    if title:
        print(f"\n  ┌{line}┐")
        print(f"  │  {title:<48}│")
        print(f"  └{line}┘")
    else:
        print(f"  {line}")


def pause():
    input("\n  [Press ENTER to continue]")


def print_path_results(label: str, origin: str, result):
    """Shared helper – prints shortest path results for both algorithms."""
    if isinstance(result, str):
        print(f"  {result}")
        return
    print(f"\n  Cheapest routes from '{origin}' ({label}):")
    for dest, (cost, path) in result.items():
        if dest == origin:
            continue
        cost_str = str(cost) if cost != float('inf') else "unreachable"
        path_str = " -> ".join(path) if path else "no path"
        print(f"    {dest:<15}  cost={cost_str:<8}  path: {path_str}")


# ══════════════════════════════════════════════
#  MENU HANDLERS
# ══════════════════════════════════════════════

def menu_graph():
    sep("PHASE 1 - Flight Network (Graph)")
    graph.display()
    pause()


def menu_dijkstra():
    sep("PHASE 1 - Dijkstra Shortest Paths")
    origin = input("  Enter origin airport: ").strip()
    result = dijkstra.shortest_path(graph.graph, origin)
    print_path_results("Dijkstra", origin, result)
    pause()


def menu_bellman_ford():
    sep("D1 - Bellman-Ford Shortest Path (step-by-step)")
    origin = input("  Enter origin airport: ").strip()
    result = bellman.shortest_path(graph.graph, origin, show_steps=True)
    print_path_results("Bellman-Ford", origin, result)
    pause()


def menu_compare_algorithms():
    sep("D1 - Dijkstra vs Bellman-Ford (Full Illustration)")
    origin = input("  Enter origin airport: ").strip()
    compare_shortest_paths(graph.graph, origin)
    pause()


def menu_mst():
    sep("PHASE 1 - Minimum Spanning Tree (Kruskal)")
    edges, total = kruskal.mst(graph.graph)
    if not edges:
        print("  MST could not be built (empty graph).")
    else:
        print(f"\n  MST edges ({len(edges)} connections):")
        for u, v, w in edges:
            print(f"    {u}  --{w}--  {v}")
        print(f"\n  Total MST cost: {total}")
    pause()


def menu_priority():
    sep("PHASE 2 - Priority Check-in (Max-Heap)")
    print("  1. Add passenger")
    print("  2. Serve next passenger")
    print("  3. Peek next passenger")
    print("  4. Queue size")
    choice = input("  Choice: ").strip()

    if choice == "1":
        name  = input("  Passenger name: ").strip()
        level = input("  Ticket class (Platinum/Gold/Silver/Economy): ").strip()
        try:
            check_in.add_passenger(name, level)
            print(f"  OK  {name} ({level}) added to check-in queue.")
        except ValueError as e:
            print(f"  ERR {e}")

    elif choice == "2":
        result = check_in.serve()
        if isinstance(result, dict):
            print(f"  OK  Serving: {result['name']}  [{result['class']}]")
        else:
            print(f"  {result}")

    elif choice == "3":
        result = check_in.peek()
        if isinstance(result, dict):
            print(f"  Next: {result['name']}  [{result['class']}]")
        else:
            print(f"  {result}")

    elif choice == "4":
        print(f"  Passengers waiting: {check_in.size()}")

    pause()


def menu_queue_stack():
    sep("PHASE 2 - Boarding Queue (FIFO) & Cargo Stack (LIFO)")
    print("  1. Add to boarding queue")
    print("  2. Board next passenger (dequeue)")
    print("  3. Load cargo bag (push)")
    print("  4. Unload cargo bag (pop)")
    print("  5. Display queue and stack")
    choice = input("  Choice: ").strip()

    if choice == "1":
        name = input("  Passenger name: ").strip()
        try:
            boarding.add(name)
            print(f"  OK  {name} added to boarding queue.")
        except ValueError as e:
            print(f"  ERR {e}")

    elif choice == "2":
        print(f"  Boarding: {boarding.remove()}")

    elif choice == "3":
        item = input("  Cargo item: ").strip()
        try:
            cargo.push(item)
            print(f"  OK  '{item}' loaded into cargo hold.")
        except ValueError as e:
            print(f"  ERR {e}")

    elif choice == "4":
        print(f"  Unloaded: {cargo.pop()}")

    elif choice == "5":
        boarding.display()
        cargo.display()

    pause()


def menu_search():
    sep("PHASE 3 - BST / AVL Price Search & Hash Table PNR Lookup")
    print("  1. BST range query (flight prices)")
    print("  2. AVL range query (flight prices)")
    print("  3. PNR lookup (Hash Table)")
    print("  4. Add new PNR record")
    print("  5. Show all values inorder (BST & AVL)")
    choice = input("  Choice: ").strip()

    if choice == "1":
        low  = int(input("  Min price: "))
        high = int(input("  Max price: "))
        res  = bst.range_query(low, high)
        print(f"  BST prices in [{low}-{high}]: {res if res else 'none found'}")

    elif choice == "2":
        low  = int(input("  Min price: "))
        high = int(input("  Max price: "))
        res  = avl.range_query(low, high)
        print(f"  AVL prices in [{low}-{high}]: {res if res else 'none found'}")

    elif choice == "3":
        pnr = input("  Enter PNR: ").strip()
        print(f"  Result: {hash_tbl.get(pnr)}")

    elif choice == "4":
        pnr  = input("  PNR code: ").strip()
        name = input("  Passenger name: ").strip()
        seat = input("  Seat: ").strip()
        cls  = input("  Class: ").strip()
        hash_tbl.add(pnr, {"name": name, "seat": seat, "class": cls})
        print(f"  OK  PNR '{pnr}' added.")

    elif choice == "5":
        print(f"  BST inorder (sorted): {bst.inorder()}")
        print(f"  AVL inorder (sorted): {avl.inorder()}")

    pause()


def menu_kmp():
    sep("PHASE 4 - KMP Passenger Name Search")
    manifest = input("  Enter flight manifest text: ").strip()
    pattern  = input("  Enter name/pattern to find: ").strip()
    indices  = kmp.search(manifest, pattern)
    if indices:
        print(f"  OK  Pattern '{pattern}' found at position(s): {indices}")
    else:
        print(f"  --  Pattern '{pattern}' not found in manifest.")
    pause()


def menu_sort():
    sep("PHASE 4 - Sorting Flight Schedules")
    print("  1. Enter custom data")
    print("  2. Use sample departure times")
    choice = input("  Choice: ").strip()

    if choice == "1":
        raw  = input("  Enter numbers separated by spaces: ")
        data = [int(x) for x in raw.split() if x.isdigit()]
    else:
        # Fixed: no leading-zero octal literals; use plain integers
        data = [1430, 600, 1800, 945, 2200, 1115, 730, 1645]
        print(f"  Sample departure times: {data}")

    if not data:
        print("  No data to sort.")
        pause()
        return

    result = compare_sorts(data)

    print(f"\n  QuickSort result : {result['quick_result']}")
    print(f"  MergeSort result : {result['merge_result']}")
    print(f"\n  QuickSort time   : {result['quick_time_us']} us")
    print(f"  MergeSort time   : {result['merge_time_us']} us")
    print(f"  Faster algorithm : {result['winner']}")
    pause()


def menu_routes():
    sep("PHASE 5 - Backtracking Route Finder")
    print("  1. Find all routes between two airports")
    print("  2. Find alternative routes (blocked hub)")
    choice = input("  Choice: ").strip()

    start = input("  Origin airport      : ").strip()
    end   = input("  Destination airport : ").strip()

    if choice == "2":
        hub    = input("  Blocked hub airport : ").strip()
        routes = router.find_with_blocked_hub(graph.graph, start, end, hub)
        print(f"\n  Routes from {start} to {end} avoiding '{hub}':")
    else:
        routes = router.find(graph.graph, start, end)
        print(f"\n  All routes from {start} to {end}:")

    if not routes:
        print("  No routes found.")
    else:
        for i, route in enumerate(routes, 1):
            print(f"  Route {i}: {' -> '.join(route)}")
    pause()


# ══════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════
def main():
    setup()
    print("\n  ╔══════════════════════════════════════╗")
    print("  ║   SkyNet Aviation Logistics System   ║")
    print("  ╚══════════════════════════════════════╝")

    menu = {
        "1": ("Show Flight Network (Graph)",               menu_graph),
        "2": ("Dijkstra  - Shortest Path",                 menu_dijkstra),
        "3": ("Bellman-Ford - Shortest Path (steps)",      menu_bellman_ford),
        "4": ("D1 - Dijkstra vs Bellman-Ford (compare)",  menu_compare_algorithms),
        "5": ("Kruskal  - Minimum Spanning Tree",          menu_mst),
        "6": ("Priority Check-in (Heap)",                  menu_priority),
        "7": ("Boarding Queue & Cargo Stack",              menu_queue_stack),
        "8": ("BST / AVL Price Search + PNR Lookup",       menu_search),
        "9": ("KMP Passenger Name Search",                 menu_kmp),
        "A": ("Sort Flight Schedules (Quick & Merge)",     menu_sort),
        "B": ("Route Finder (Backtracking)",               menu_routes),
        "0": ("Exit",                                      None),
    }

    while True:
        print("\n  ┌──────────────────────────────────────────┐")
        print("  │              MAIN MENU                   │")
        print("  ├──────────────────────────────────────────┤")
        for key, (label, _) in menu.items():
            print(f"  │  [{key}]  {label:<38}│")
        print("  └──────────────────────────────────────────┘")

        user_choice = input("  Select option: ").strip().upper()

        if user_choice == "0":
            print("\n  Goodbye - SkyNet shutting down.\n")
            break
        elif user_choice in menu:
            _, handler = menu[user_choice]
            handler()
        else:
            print("  Invalid option. Please try again.")


if __name__ == "__main__":
    main()