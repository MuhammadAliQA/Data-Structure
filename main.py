from graph     import Graph, Dijkstra, Kruskal
from passenger import PriorityCheckIn, BoardingQueue, CargoStack
from search    import BST, AVLTree, HashTable, KMP
from sorting   import QuickSort, MergeSort, compare_sorts
from routing   import RouteFinder


# ══════════════════════════════════════════════════════
#  Global ob'yektlar
# ══════════════════════════════════════════════════════
g     = Graph()
d     = Dijkstra()
k     = Kruskal()
check = PriorityCheckIn()
queue = BoardingQueue()
cargo = CargoStack()
bst   = BST()
avl   = AVLTree()
avl_root = None
ht    = HashTable()
kmp   = KMP()
rf    = RouteFinder()


def divider(char="─", width=50):
    print(char * width)


def header(title):
    divider("═")
    print(f"  ✈  {title}")
    divider("═")


# ══════════════════════════════════════════════════════
#  Boshlang'ich ma'lumotlar
# ══════════════════════════════════════════════════════
def setup():
    # Graf (directed + undirected for MST)
    for city in ["Tashkent", "Dubai", "Istanbul", "London"]:
        g.add_airport(city)

    for src, dst, cost in [
        ("Tashkent", "Dubai",    500),
        ("Tashkent", "Istanbul", 400),
        ("Dubai",    "London",   700),
        ("Istanbul", "London",   600),
    ]:
        g.add_undirected_flight(src, dst, cost)

    # BST: narxlar
    for price in [500, 400, 700, 600, 350, 800, 250]:
        bst.insert(price)

    # AVL Tree
    global avl_root
    for price in [500, 400, 700, 600, 350, 800, 250]:
        avl_root = avl.insert(avl_root, price)

    # Hash Table: PNR → yo'lovchi
    for pnr, name in [
        ("PNR001", "Ali Karimov"),
        ("PNR002", "John Smith"),
        ("PNR003", "Sara Lee"),
        ("PNR004", "Bobur Rahimov"),
    ]:
        ht.add(pnr, name)


# ══════════════════════════════════════════════════════
#  Menu handlerlari
# ══════════════════════════════════════════════════════
def show_graph():
    header("PHASE 1 – Graf tarmog'i")
    g.display()


def show_dijkstra():
    header("PHASE 1 – Dijkstra: Eng qisqa yo'l")
    start = "Tashkent"
    dists, prev = d.shortest_path(g.graph, start)
    if dists is None:
        print(prev)
        return

    print(f"  Boshlanish: {start}\n")
    print(f"  {'Manzil':<14} {'Narx ($)':>10}   Yo'l")
    divider()
    for city in ["Dubai", "Istanbul", "London"]:
        cost = dists[city]
        path = d.get_path(prev, start, city)
        route = " → ".join(path) if path else "yo'q"
        marker = "  ★" if city == "London" else "   "
        print(f"{marker} {city:<14} {cost:>10}   {route}")
    divider()
    print("  ★ = eng uzoq manzil (Dijkstra optimal yo'li)")


def show_mst():
    header("PHASE 1 – Kruskal: Minimum Spanning Tree")
    edges, total = k.mst(g.graph)
    print(f"  {'Edge':<30} {'Narx ($)':>8}")
    divider()
    for u, v, w in edges:
        print(f"  {u} ↔ {v:<20} {w:>8}")
    divider()
    print(f"  Umumiy MST narxi:          ${total}")
    print(f"\n  Bu {len(edges)} ta edge barcha {len(g.graph)} ta aeroportni")
    print("  minimal xarajat bilan bog'laydi.")


def show_priority():
    header("PHASE 2 – Priority Queue (Max-Heap Check-In)")

    passengers = [
        ("Ali Karimov",   "Economy"),
        ("Sara Lee",      "Platinum"),
        ("Bobur Rahimov", "Gold"),
        ("John Smith",    "Platinum"),
        ("Malika Yusupova","Economy"),
    ]
    print("  Yo'lovchilar navbatga qo'shilmoqda:\n")
    for name, level in passengers:
        check.add_passenger(name, level)

    print(f"\n  Navbatdagi yo'lovchilar soni: {check.size()}")
    print(f"\n  Xizmat tartibi (ustuvorlik bo'yicha):")
    divider()
    while check.size() > 0:
        print(check.serve())
    divider()


def show_queue_stack():
    header("PHASE 2 – Boarding Queue (FIFO) & Cargo Stack (LIFO)")

    print("  [BOARDING GATE – FIFO Queue]")
    for p in ["Bobur", "Sara", "Ali"]:
        queue.add(p)
    print()
    print(f"  Boarding boshlandi ({queue.size()} kishi):")
    while queue.size() > 0:
        print(queue.remove())

    print()
    print("  [CARGO HOLD – LIFO Stack]")
    for item in ["Buggy #1", "Suitcase #2", "Box #3"]:
        cargo.push(item)
    print()
    print(f"  Yuklar tushirilmoqda ({cargo.size()} dona):")
    while cargo.size() > 0:
        print(cargo.pop())


def show_search():
    header("PHASE 3 – Trees & Hashing")

    # BST
    print("  [BST – Binary Search Tree]")
    print(f"  Barcha narxlar (sorted): {bst.inorder()}")
    low, high = 400, 650
    found = bst.range_query(low, high)
    print(f"  ${low}–${high} oralig'idagi narxlar: {found}")
    print(f"  $600 bor? {bst.search(600)}   $999 bor? {bst.search(999)}")

    print()
    print("  [AVL Tree – Balanslangan BST]")
    print(f"  AVL inorder: {avl.inorder(avl_root)}")

    print()
    print("  [Hash Table – PNR qidirish O(1)]")
    for pnr in ["PNR001", "PNR003", "PNR999"]:
        result = ht.get(pnr)
        if result:
            print(f"  {pnr} → {result}")
        else:
            print(f"  {pnr} → Topilmadi!")
    print(f"  Load factor: {ht.load_factor()}")

    print()
    print("  [KMP – String Qidirish Algoritmi]")
    manifest = "Ali Karimov, Sara Lee, Bobur Rahimov, John Smith"
    tests = ["Sara", "Bobur", "Omar"]
    for pattern in tests:
        positions = kmp.search(manifest, pattern)
        if positions:
            print(f"  '{pattern}' topildi – indeks: {positions}")
        else:
            print(f"  '{pattern}' – manifestda yo'q.")


def show_sort():
    header("PHASE 4 – Sorting: QuickSort vs MergeSort")

    data = [850, 200, 620, 410, 990, 130, 750, 380, 560, 240]
    print(f"  Kiruvchi ma'lumot: {data}\n")

    res_q, res_m, time_q, time_m = compare_sorts(data)

    print(f"  {'Algoritm':<14} {'Natija':<45} {'Vaqt (µs)':>10}")
    divider()
    print(f"  {'QuickSort':<14} {str(res_q):<45} {time_q:>10.2f}")
    print(f"  {'MergeSort':<14} {str(res_m):<45} {time_m:>10.2f}")
    divider()
    print(f"\n  QuickSort: O(n log n) o'rtacha, O(n²) eng yomon holat")
    print(f"  MergeSort: O(n log n) har doim, lekin O(n) qo'shimcha xotira")

    faster = "QuickSort" if time_q < time_m else "MergeSort"
    print(f"\n  Bu o'tishda tezroq: {faster}")


def show_routes():
    header("PHASE 5 – Backtracking: Muqobil Marshrut")

    start, end = "Tashkent", "London"
    print(f"  Barchа yo'llar: {start} → {end}\n")

    all_paths = rf.find(g.graph, start, end)
    for i, path in enumerate(all_paths, 1):
        route = " → ".join(path)
        print(f"  Yo'l {i}: {route}")

    print()
    blocked = "Dubai"
    print(f"  '{blocked}' yopilganda muqobil yo'llar:\n")
    alt_paths = rf.find(g.graph, start, end, blocked=blocked)
    if alt_paths:
        for i, path in enumerate(alt_paths, 1):
            route = " → ".join(path)
            print(f"  Yo'l {i}: {route}")
    else:
        print(f"  Muqobil yo'l topilmadi!")


# ══════════════════════════════════════════════════════
#  Asosiy menyu
# ══════════════════════════════════════════════════════
MENU = {
    "1": ("Graf tarmog'i",           show_graph),
    "2": ("Dijkstra (eng qisqa yo'l)", show_dijkstra),
    "3": ("MST – Kruskal",           show_mst),
    "4": ("Priority Check-In",       show_priority),
    "5": ("Boarding Queue & Cargo",  show_queue_stack),
    "6": ("Trees & Hash & KMP",      show_search),
    "7": ("Sort taqqoslash",         show_sort),
    "8": ("Backtracking marshrut",   show_routes),
    "0": ("Chiqish",                 None),
}


def print_menu():
    print()
    divider("═")
    print("  ✈  SKYNET AVIATSIYA BOSHQARUV TIZIMI")
    divider("═")
    for key, (label, _) in MENU.items():
        print(f"  {key}.  {label}")
    divider("─")


def main():
    setup()
    while True:
        print_menu()
        choice = input("  Tanlang: ").strip()
        if choice == "0":
            print("\n  SkyNet tizimidan chiqildi. Xayr!\n")
            break
        if choice in MENU:
            _, handler = MENU[choice]
            print()
            handler()
        else:
            print("  ⚠  Noto'g'ri tanlov. Qayta urinib ko'ring.")


if __name__ == "__main__":
    main()