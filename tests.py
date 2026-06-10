from graph     import Graph, Dijkstra, Kruskal
from passenger import PriorityCheckIn, BoardingQueue, CargoStack
from search    import BST, AVLTree, HashTable, KMP
from sorting   import QuickSort, MergeSort
from routing   import RouteFinder

passed = 0
failed = 0


def check(nom, holat, kutilgan=None, kelgan=None):
    global passed, failed
    if holat:
        print(f"  PASS  {nom}")
        passed += 1
    else:
        print(f"  FAIL  {nom}")
        if kutilgan is not None:
            print(f"        Kutilgan : {kutilgan}")
            print(f"        Kelgan   : {kelgan}")
        failed += 1


def boʻlim(nom):
    print(f"\n{'=' * 50}")
    print(f"  {nom}")
    print(f"{'=' * 50}")


def natija():
    jami = passed + failed
    print(f"\n{'=' * 50}")
    print(f"  NATIJA: {passed}/{jami} test muvaffaqiyatli")
    if failed == 0:
        print("  Barcha testlar PASS!")
    else:
        print(f"  {failed} ta test FAIL!")
    print(f"{'=' * 50}\n")


# ── GRAPH ────────────────────────────────────────────
boʻlim("PHASE 1 – Graph")

g = Graph()
g.add_airport("A")
g.add_airport("B")
g.add_airport("C")
g.add_undirected_flight("A", "B", 10)
g.add_undirected_flight("B", "C", 20)

check("Aeroport qo'shildi",             "A" in g.graph and "B" in g.graph and "C" in g.graph)
check("A→B flight mavjud",              ("B", 10) in g.graph["A"])
check("Undirected: B→A ham mavjud",     ("A", 10) in g.graph["B"])
check("Bo'sh grafga aeroport qo'shish", len(Graph().graph) == 0)
check("Takroriy aeroport qo'shilmaydi", len(g.graph) == 3)

# ── DIJKSTRA ─────────────────────────────────────────
boʻlim("PHASE 1 – Dijkstra")

d   = Dijkstra()
net = {
    "Tashkent": [("Dubai", 500), ("Istanbul", 400)],
    "Dubai":    [("London", 700)],
    "Istanbul": [("London", 600)],
    "London":   [],
}
dists, prev = d.shortest_path(net, "Tashkent")

check("Start masofasi 0",                   dists["Tashkent"] == 0)
check("Tashkent→Dubai = 500",               dists["Dubai"] == 500)
check("Tashkent→Istanbul = 400",            dists["Istanbul"] == 400)
check("Tashkent→London = 1000",             dists["London"] == 1000,          1000, dists["London"])
check("Yo'l: Tashkent→Istanbul→London",
      d.get_path(prev, "Tashkent", "London") == ["Tashkent", "Istanbul", "London"],
      ["Tashkent", "Istanbul", "London"], d.get_path(prev, "Tashkent", "London"))
check("Bo'sh grafda xato qaytadi",          d.shortest_path({}, "A")[0] is None)
check("Noto'g'ri start – xato qaytadi",     d.shortest_path(net, "Paris")[0] is None)
check("Bir tugunli grafda start=0",         d.shortest_path({"X": []}, "X")[0]["X"] == 0)

# ── KRUSKAL ──────────────────────────────────────────
boʻlim("PHASE 1 – Kruskal MST")

k = Kruskal()
mg = {
    "A": [("B", 1), ("C", 4)],
    "B": [("A", 1), ("C", 2), ("D", 5)],
    "C": [("A", 4), ("B", 2), ("D", 1)],
    "D": [("B", 5), ("C", 1)],
}
edges, total = k.mst(mg)
check("MST edge soni = V-1 = 3",    len(edges) == 3,  3,  len(edges))
check("MST umumiy narxi = 4",        total == 4,        4,  total)

cg = {"X": [("Y", 10), ("Z", 6)], "Y": [("X", 10), ("Z", 5)], "Z": [("X", 6), ("Y", 5)]}
k2 = Kruskal()
e2, t2 = k2.mst(cg)
check("Sikliy grafda MST edge soni = 2", len(e2) == 2)
check("Sikliy grafda narx = 11",         t2 == 11, 11, t2)

# ── PRIORITY QUEUE ───────────────────────────────────
boʻlim("PHASE 2 – Priority Queue (Max-Heap)")

p = PriorityCheckIn()
check("Bo'sh navbatda serve – xato xabari", "bo'sh" in p.serve().lower())

p.add_passenger("Economy1", "Economy")
p.add_passenger("Platinum1", "Platinum")
p.add_passenger("Gold1",     "Gold")
p.add_passenger("Platinum2", "Platinum")

r1, r2, r3 = p.serve(), p.serve(), p.serve()
check("Birinchi Platinum chiqadi",          "Platinum" in r1)
check("Ikkinchi ham Platinum",              "Platinum" in r2)
check("Uchinchi Gold chiqadi",              "Gold" in r3)

p2 = PriorityCheckIn()
p2.add_passenger("First",  "Platinum")
p2.add_passenger("Second", "Platinum")
a, b = p2.serve(), p2.serve()
check("Bir xil darajada FIFO tartibi",      "First" in a and "Second" in b)

# ── QUEUE VA STACK ───────────────────────────────────
boʻlim("PHASE 2 – BoardingQueue (FIFO) & CargoStack (LIFO)")

q = BoardingQueue()
check("Bo'sh queuedan remove – xato", "bo'sh" in q.remove().lower())
q.add("Ali"); q.add("Sara"); q.add("John")
check("FIFO: Ali birinchi chiqadi",   "Ali"  in q.remove())
check("FIFO: Sara ikkinchi",          "Sara" in q.remove())
check("Queue hajmi = 1",              q.size() == 1)

s = CargoStack()
check("Bo'sh stackdan pop – xato",    "bo'sh" in s.pop().lower())
s.push("Bag1"); s.push("Bag2"); s.push("Bag3")
check("LIFO: Bag3 birinchi chiqadi",  "Bag3" in s.pop())
check("LIFO: Bag2 ikkinchi",          "Bag2" in s.pop())
check("Stack hajmi = 1",              s.size() == 1)

# ── BST ──────────────────────────────────────────────
boʻlim("PHASE 3 – BST")

bst = BST()
check("Bo'sh BST search False",       bst.search(100) == False)
check("Bo'sh BST range_query = []",   bst.range_query(0, 999) == [])

for v in [500, 300, 700, 200, 400, 600, 800]:
    bst.insert(v)

check("Inorder tartiblangan",         bst.inorder() == [200, 300, 400, 500, 600, 700, 800])
check("Search: 400 bor",              bst.search(400) == True)
check("Search: 999 yo'q",             bst.search(999) == False)
rq = bst.range_query(300, 600)
check("Range [300,600] to'g'ri",      rq == [300, 400, 500, 600], [300, 400, 500, 600], rq)
check("Range bo'sh oraliq",           bst.range_query(900, 1000) == [])

# ── AVL ──────────────────────────────────────────────
boʻlim("PHASE 3 – AVL Tree")

avl  = AVLTree()
root = None
for v in [10, 20, 30, 40, 50, 25]:
    root = avl.insert(root, v)

check("AVL inorder tartiblangan",     avl.inorder(root) == [10, 20, 25, 30, 40, 50])
check("AVL height balanslangan ≤ 4",  root.height <= 4)
check("Takroriy qiymat qo'shilmaydi", avl.inorder(avl.insert(root, 30)) == [10, 20, 25, 30, 40, 50])

# ── HASH TABLE ───────────────────────────────────────
boʻlim("PHASE 3 – Hash Table")

ht = HashTable()
check("Mavjud bo'lmagan key – None",  ht.get("PNR999") is None)
ht.add("PNR001", "Ali")
ht.add("PNR002", "Sara")
ht.add("PNR003", "Bobur")
check("get() to'g'ri qaytaradi",      ht.get("PNR001") == "Ali")
check("Mavjud key yangilanadi",        (ht.add("PNR001", "Ali2") or True) and ht.get("PNR001") == "Ali2")
check("delete() ishlaydi",            ht.delete("PNR002") == True and ht.get("PNR002") is None)
check("Yo'q keyni delete – False",    ht.delete("PNR999") == False)

# ── KMP ──────────────────────────────────────────────
boʻlim("PHASE 3 – KMP")

kmp = KMP()
check("Pattern topildi",              kmp.contains("Ali Karimov", "Karimov") == True)
check("Pattern topilmadi",            kmp.contains("Ali Karimov", "Smith")   == False)
pos = kmp.search("abababab", "ab")
check("Bir necha match – to'g'ri",    pos == [0, 2, 4, 6], [0, 2, 4, 6], pos)
check("Bo'sh pattern – []",           kmp.search("hello", "") == [])
check("Pattern > matn – []",          kmp.search("hi", "hello world") == [])
check("To'liq mos – [0]",             kmp.search("abc", "abc") == [0])

# ── SORTING ──────────────────────────────────────────
boʻlim("PHASE 4 – QuickSort & MergeSort")

qs  = QuickSort()
ms  = MergeSort()
arr = [64, 34, 25, 12, 22, 11, 90]
exp = [11, 12, 22, 25, 34, 64, 90]

check("QuickSort to'g'ri",             qs.sort(arr) == exp, exp, qs.sort(arr))
check("MergeSort to'g'ri",             ms.sort(arr) == exp, exp, ms.sort(arr))
check("QuickSort bo'sh massiv",        qs.sort([]) == [])
check("MergeSort bo'sh massiv",        ms.sort([]) == [])
check("QuickSort bir element",         qs.sort([42]) == [42])
check("QuickSort tartiblangan massiv", qs.sort([1,2,3,4,5]) == [1,2,3,4,5])
check("MergeSort teskari tartib",      ms.sort([5,4,3,2,1]) == [1,2,3,4,5])
check("QuickSort takroriy elementlar", qs.sort([3,1,4,1,5]) == sorted([3,1,4,1,5]))
check("Ikkalasi bir xil natija",       qs.sort(arr) == ms.sort(arr))
orig = [5, 3, 1]; _ = qs.sort(orig)
check("Asl massiv o'zgarmadi",         orig == [5, 3, 1])

# ── BACKTRACKING ─────────────────────────────────────
boʻlim("PHASE 5 – Backtracking")

rf   = RouteFinder()
net2 = {
    "Tashkent": [("Dubai", 500),    ("Istanbul", 400)],
    "Dubai":    [("Tashkent", 500), ("London", 700)],
    "Istanbul": [("Tashkent", 400), ("London", 600)],
    "London":   [("Dubai", 700),    ("Istanbul", 600)],
}

paths = rf.find(net2, "Tashkent", "London")
check("2 ta yo'l topiladi",           len(paths) == 2, 2, len(paths))
check("Dubai orqali yo'l bor",        ["Tashkent", "Dubai", "London"] in paths)

pb = rf.find(net2, "Tashkent", "London", blocked="Dubai")
check("Dubai yopilganda 1 ta yo'l",   len(pb) == 1, 1, len(pb))
check("Istanbul orqali yo'l qoladi",  ["Tashkent", "Istanbul", "London"] in pb)
check("Noto'g'ri start – []",         rf.find(net2, "Paris", "London") == [])
check("Start = End – [[London]]",     rf.find(net2, "London", "London") == [["London"]])
check("Bo'sh grafda yo'l yo'q",       rf.find({}, "A", "B") == [])

# ── NATIJA ───────────────────────────────────────────
natija()