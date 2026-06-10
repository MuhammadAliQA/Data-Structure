from graph     import Graph, Dijkstra, Kruskal, BellmanFord, Prim
from passenger import PriorityCheckIn, BoardingQueue, CargoStack
from search    import BST, AVLTree, HashTable, KMP
from sorting   import QuickSort, MergeSort, compare_sorts, full_compare
from routing   import RouteFinder

g        = Graph()
d        = Dijkstra()
k        = Kruskal()
bf       = BellmanFord()
prim     = Prim()
check    = PriorityCheckIn()
queue    = BoardingQueue()
cargo    = CargoStack()
bst      = BST()
avl      = AVLTree()
avl_root = None
ht       = HashTable()
kmp      = KMP()
rf       = RouteFinder()


def chiziq(belgi="─", uzunlik=50):
    print(belgi * uzunlik)


def sarlavha(nom):
    chiziq("═")
    print(f"  {nom}")
    chiziq("═")


def setup():
    for shahar in ["Tashkent", "Dubai", "Istanbul", "London"]:
        g.add_airport(shahar)
    for src, dst, narx in [
        ("Tashkent", "Dubai",    500),
        ("Tashkent", "Istanbul", 400),
        ("Dubai",    "London",   700),
        ("Istanbul", "London",   600),
    ]:
        g.add_undirected_flight(src, dst, narx)
    for narx in [500, 400, 700, 600, 350, 800, 250]:
        bst.insert(narx)
    global avl_root
    for narx in [500, 400, 700, 600, 350, 800, 250]:
        avl_root = avl.insert(avl_root, narx)
    for pnr, ism in [
        ("PNR001", "Ali Karimov"),
        ("PNR002", "John Smith"),
        ("PNR003", "Sara Lee"),
        ("PNR004", "Bobur Rahimov"),
    ]:
        ht.add(pnr, ism)


def show_graph():
    sarlavha("PHASE 1 – Reys tarmog'i")
    g.display()


def show_dijkstra():
    sarlavha("PHASE 1 – Dijkstra: Eng qisqa yo'l")
    start = "Tashkent"
    dists, prev = d.shortest_path(g.graph, start)
    if dists is None:
        print(f"  {prev}")
        return
    print(f"  Boshlanish: {start}\n")
    print(f"  {'Manzil':<14} {'Narx ($)':>10}   Yo'l")
    chiziq()
    for shahar in ["Dubai", "Istanbul", "London"]:
        narx  = dists[shahar]
        yol   = d.get_path(prev, start, shahar)
        matn  = " → ".join(yol) if yol else "yo'q"
        belgi = "  *" if shahar == "London" else "   "
        print(f"{belgi} {shahar:<14} {narx:>10}   {matn}")
    chiziq()
    print("  * = eng arzon umumiy marshrut")


def show_mst():
    sarlavha("PHASE 1 – Kruskal: Minimum Spanning Tree")
    edges, total = k.mst(g.graph)
    print(f"  {'Ulanish':<32} {'Narx ($)':>8}")
    chiziq()
    for u, v, w in edges:
        print(f"  {u} -- {v:<22} {w:>8}")
    chiziq()
    print(f"  Umumiy narx: ${total}")
    print(f"  {len(edges)} ta ulanish, {len(g.graph)} ta aeroport")


def show_priority():
    sarlavha("PHASE 2 – Priority Queue (Max-Heap)")
    yolovchilar = [
        ("Ali Karimov",    "Economy"),
        ("Sara Lee",       "Platinum"),
        ("Bobur Rahimov",  "Gold"),
        ("John Smith",     "Platinum"),
        ("Malika Yusupova","Economy"),
    ]
    print("  Navbatga qo'shilmoqda:\n")
    for ism, daraja in yolovchilar:
        check.add_passenger(ism, daraja)
    print(f"\n  Jami: {check.size()} kishi")
    print("\n  Xizmat tartibi:")
    chiziq()
    while check.size() > 0:
        print(check.serve())
    chiziq()


def show_queue_stack():
    sarlavha("PHASE 2 – Boarding Queue (FIFO) va Cargo Stack (LIFO)")
    print("  [ BOARDING GATE – FIFO ]")
    for p in ["Bobur", "Sara", "Ali"]:
        queue.add(p)
    print(f"\n  Boarding ({queue.size()} kishi):")
    while queue.size() > 0:
        print(queue.remove())

    print("\n  [ YUKXONA – LIFO Stack ]")
    for yuk in ["Buggy #1", "Suitcase #2", "Box #3"]:
        cargo.push(yuk)
    print(f"\n  Yuklar tushirilmoqda ({cargo.size()} dona):")
    while cargo.size() > 0:
        print(cargo.pop())


def show_search():
    sarlavha("PHASE 3 – BST, AVL, Hash Table, KMP")

    print("  [ BST ]")
    print(f"  Barcha narxlar: {bst.inorder()}")
    low, high = 400, 650
    print(f"  ${low}–${high} oralig'i: {bst.range_query(low, high)}")
    print(f"  $600 bor? {bst.search(600)}   $999 bor? {bst.search(999)}")

    print("\n  [ AVL Tree ]")
    print(f"  Inorder: {avl.inorder(avl_root)}")

    print("\n  [ Hash Table ]")
    for pnr in ["PNR001", "PNR003", "PNR999"]:
        natija = ht.get(pnr)
        print(f"  {pnr} --> {natija if natija else 'Topilmadi'}")
    print(f"  Load factor: {ht.load_factor()}")

    print("\n  [ KMP ]")
    manifest = "Ali Karimov, Sara Lee, Bobur Rahimov, John Smith"
    for pattern in ["Sara", "Bobur", "Omar"]:
        pozitsiyalar = kmp.search(manifest, pattern)
        if pozitsiyalar:
            print(f"  '{pattern}' topildi – indeks: {pozitsiyalar}")
        else:
            print(f"  '{pattern}' – yo'q")


def show_sort():
    sarlavha("PHASE 4 – QuickSort vs MergeSort")
    data = [850, 200, 620, 410, 990, 130, 750, 380, 560, 240]
    print(f"  Kiruvchi: {data}\n")
    res_q, res_m, time_q, time_m, mem_q, mem_m = full_compare(data)
    print(f"  {'Algoritm':<12} {'Natija':<44} {'Vaqt(µs)':>9}  {'Xotira(B)':>9}")
    chiziq()
    print(f"  {'QuickSort':<12} {str(res_q):<44} {time_q:>9.2f}  {mem_q:>9}")
    print(f"  {'MergeSort':<12} {str(res_m):<44} {time_m:>9.2f}  {mem_m:>9}")
    chiziq()
    print(f"\n  Tezroq:    {'QuickSort' if time_q < time_m else 'MergeSort'}")
    print(f"  Tejamroq:  {'QuickSort' if mem_q < mem_m else 'MergeSort'}")
    print("\n  QuickSort: O(n log n) ort., O(n²) eng yomon, O(log n) xotira")
    print("  MergeSort: O(n log n) har doim,          O(n) xotira")


def show_compare_sp():
    sarlavha("D1 – Dijkstra vs Bellman-Ford")
    dists_d, _ = d.shortest_path(g.graph, "Tashkent")
    dists_b, _ = bf.shortest_path(g.graph, "Tashkent")
    print(f"  {'Manzil':<14} {'Dijkstra':>10}  {'Bellman-Ford':>13}  {'Mos?':>5}")
    chiziq()
    for shahar in ["Dubai", "Istanbul", "London"]:
        dd    = dists_d[shahar]
        db    = dists_b[shahar]
        print(f"  {shahar:<14} {dd:>10}  {db:>13}  {'Ha' if dd==db else 'Yo\'q':>5}")
    chiziq()
    print(f"\n  {'Xususiyat':<26} {'Dijkstra':>14}  {'Bellman-Ford':>13}")
    chiziq()
    for xus, dj, bell in [
        ("Vaqt",                "O((V+E)logV)", "O(V·E)"),
        ("Manfiy edge",         "Yo'q",         "Ha"),
        ("Manfiy sikl aniqlash","Yo'q",         "Ha"),
        ("Zich grafda",         "Tezroq",       "Sekinroq"),
    ]:
        print(f"  {xus:<26} {dj:>14}  {bell:>13}")
    chiziq()


def show_prim():
    sarlavha("D1 – Kruskal vs Prim (MST)")
    edges_k, total_k = k.mst(g.graph)
    edges_p, total_p = prim.mst(g.graph, start="Tashkent")
    print(f"  {'Kruskal':<36} {'Prim (start=Tashkent)'}")
    chiziq()
    for i in range(max(len(edges_k), len(edges_p))):
        ek = f"{edges_k[i][0]} -- {edges_k[i][1]} (${edges_k[i][2]})" if i < len(edges_k) else ""
        ep = f"{edges_p[i][0]} -> {edges_p[i][1]} (${edges_p[i][2]})" if i < len(edges_p) else ""
        print(f"  {ek:<36} {ep}")
    chiziq()
    print(f"  Kruskal jami: ${total_k}    Prim jami: ${total_p}")
    print(f"\n  {'Xususiyat':<26} {'Kruskal':>12}  {'Prim':>10}")
    chiziq()
    for xus, kr, pr in [
        ("Yondashuv",         "Edge-based",  "Node-based"),
        ("Vaqt",              "O(E log E)",  "O(E log V)"),
        ("Siyrak grafda",     "Tezroq",      "Sekinroq"),
        ("Zich grafda",       "Sekinroq",    "Tezroq"),
    ]:
        print(f"  {xus:<26} {kr:>12}  {pr:>10}")
    chiziq()


def show_routes():
    sarlavha("PHASE 5 – Backtracking: Muqobil Marshrut")
    start, end = "Tashkent", "London"
    print(f"  Barcha yo'llar: {start} → {end}\n")
    for i, yol in enumerate(rf.find(g.graph, start, end), 1):
        print(f"  Yo'l {i}: {' → '.join(yol)}")
    print()
    blocked = "Dubai"
    print(f"  '{blocked}' yopilganda:\n")
    muqobil = rf.find(g.graph, start, end, blocked=blocked)
    if muqobil:
        for i, yol in enumerate(muqobil, 1):
            print(f"  Yo'l {i}: {' → '.join(yol)}")
    else:
        print("  Muqobil yo'l topilmadi!")


MENU = {
    "1":  ("Reys tarmog'i",           show_graph),
    "2":  ("Dijkstra",                show_dijkstra),
    "3":  ("MST – Kruskal",           show_mst),
    "4":  ("Priority Check-In",       show_priority),
    "5":  ("Boarding & Cargo",        show_queue_stack),
    "6":  ("BST / AVL / Hash / KMP",  show_search),
    "7":  ("Sort taqqoslash",         show_sort),
    "8":  ("Backtracking marshrut",   show_routes),
    "9":  ("Dijkstra vs Bellman-Ford",show_compare_sp),
    "10": ("Kruskal vs Prim",         show_prim),
    "0":  ("Chiqish",                 None),
}


def menyu():
    print()
    chiziq("═")
    print("  SKYNET – Aviatsiya Boshqaruv Tizimi")
    chiziq("═")
    for key, (nom, _) in MENU.items():
        print(f"  {key:>2}.  {nom}")
    chiziq("─")


def main():
    setup()
    while True:
        menyu()
        tanlov = input("  Tanlang: ").strip()
        if tanlov == "0":
            print("\n  Chiqildi. Xayr!\n")
            break
        if tanlov in MENU:
            print()
            MENU[tanlov][1]()
        else:
            print("  Noto'g'ri tanlov!")


if __name__ == "__main__":
    main()