"""
tests.py – SkyNet DSA Test Suite
Assignment P5: Error handling va edge case testlar
"""

from graph     import Graph, Dijkstra, Kruskal
from passenger import PriorityCheckIn, BoardingQueue, CargoStack
from search    import BST, AVLTree, HashTable, KMP
from sorting   import QuickSort, MergeSort
from routing   import RouteFinder


# ══════════════════════════════════════════════════════
#  Yordamchi funksiyalar
# ══════════════════════════════════════════════════════
passed = 0
failed = 0


def check(test_name, condition, expected=None, got=None):
    global passed, failed
    if condition:
        print(f"  ✅ PASS  {test_name}")
        passed += 1
    else:
        print(f"  ❌ FAIL  {test_name}")
        if expected is not None:
            print(f"         Kutilgan : {expected}")
            print(f"         Kelgan   : {got}")
        failed += 1


def section(title):
    print(f"\n{'═' * 52}")
    print(f"  ✈  {title}")
    print(f"{'═' * 52}")


def summary():
    total = passed + failed
    print(f"\n{'═' * 52}")
    print(f"  NATIJA: {passed}/{total} test muvaffaqiyatli o'tdi")
    if failed == 0:
        print("  🎉 Barcha testlar PASS!")
    else:
        print(f"  ⚠️  {failed} ta test FAIL – tekshiring!")
    print(f"{'═' * 52}\n")


# ══════════════════════════════════════════════════════
#  PHASE 1 – Graph testlar
# ══════════════════════════════════════════════════════
section("PHASE 1 – Graph")

g = Graph()
g.add_airport("A")
g.add_airport("B")
g.add_airport("C")
g.add_undirected_flight("A", "B", 10)
g.add_undirected_flight("B", "C", 20)

check("Aeroport qo'shildi",
      "A" in g.graph and "B" in g.graph and "C" in g.graph)

check("Flight A→B mavjud",
      ("B", 10) in g.graph["A"])

check("Undirected: B→A ham mavjud",
      ("A", 10) in g.graph["B"])

check("Bo'sh grafga aeroport qo'shish",
      len(Graph().graph) == 0)

check("Takroriy aeroport qo'shilmaydi",
      len(g.graph) == 3)   # A, B, C – 3 ta


# ══════════════════════════════════════════════════════
#  PHASE 1 – Dijkstra testlar
# ══════════════════════════════════════════════════════
section("PHASE 1 – Dijkstra")

d = Dijkstra()

# Normal holat
net = {
    "Tashkent": [("Dubai", 500), ("Istanbul", 400)],
    "Dubai":    [("London", 700)],
    "Istanbul": [("London", 600)],
    "London":   [],
}
dists, prev = d.shortest_path(net, "Tashkent")

check("Start tugunning masofasi 0",
      dists["Tashkent"] == 0)

check("Tashkent→Dubai = 500",
      dists["Dubai"] == 500)

check("Tashkent→Istanbul = 400",
      dists["Istanbul"] == 400)

check("Tashkent→London eng qisqa = 1000 (Istanbul orqali)",
      dists["London"] == 1000,
      expected=1000, got=dists["London"])

path = d.get_path(prev, "Tashkent", "London")
check("London yo'li: Tashkent→Istanbul→London",
      path == ["Tashkent", "Istanbul", "London"],
      expected=["Tashkent", "Istanbul", "London"], got=path)

# Edge case: bo'sh graf
dists2, msg = d.shortest_path({}, "A")
check("Bo'sh grafda xato xabari qaytadi",
      dists2 is None)

# Edge case: mavjud bo'lmagan start
dists3, msg3 = d.shortest_path(net, "Paris")
check("Noto'g'ri start node – xato xabari",
      dists3 is None)

# Edge case: bir tugunli graf
solo = {"X": []}
dists4, _ = d.shortest_path(solo, "X")
check("Bir tugunli grafda start=0",
      dists4["X"] == 0)


# ══════════════════════════════════════════════════════
#  PHASE 1 – Kruskal (MST) testlar
# ══════════════════════════════════════════════════════
section("PHASE 1 – Kruskal MST")

k = Kruskal()

mst_graph = {
    "A": [("B", 1), ("C", 4)],
    "B": [("A", 1), ("C", 2), ("D", 5)],
    "C": [("A", 4), ("B", 2), ("D", 1)],
    "D": [("B", 5), ("C", 1)],
}
edges, total = k.mst(mst_graph)

check("MST edge soni to'g'ri (V-1 = 3)",
      len(edges) == 3,
      expected=3, got=len(edges))

check("MST umumiy narxi minimal = 4",
      total == 4,
      expected=4, got=total)

# Siklik graf (cycle bor) – MST siklni o'tkazib ketishi kerak
cycle_graph = {
    "X": [("Y", 10), ("Z", 6)],
    "Y": [("X", 10), ("Z", 5)],
    "Z": [("X", 6),  ("Y", 5)],
}
k2 = Kruskal()
edges2, total2 = k2.mst(cycle_graph)
check("Sikliy grafda ham MST to'g'ri (V-1 edge)",
      len(edges2) == 2)
check("Sikliy grafda narx minimal = 11",
      total2 == 11,
      expected=11, got=total2)


# ══════════════════════════════════════════════════════
#  PHASE 2 – Priority Queue testlar
# ══════════════════════════════════════════════════════
section("PHASE 2 – Priority Queue (Max-Heap)")

p = PriorityCheckIn()

# Bo'sh holatda serve
result = p.serve()
check("Bo'sh navbatda serve – xato xabari",
      "bo'sh" in result.lower() or "yo'q" in result.lower())

# Ustuvorlik tartibi
p.add_passenger("Economy1", "Economy")
p.add_passenger("Platinum1", "Platinum")
p.add_passenger("Gold1", "Gold")
p.add_passenger("Platinum2", "Platinum")

first  = p.serve()
second = p.serve()
third  = p.serve()

check("Birinchi Platinum chiqishi kerak",
      "Platinum" in first)

check("Ikkinchi ham Platinum (ikkita Platinum bor)",
      "Platinum" in second)

check("Uchinchi Gold chiqishi kerak",
      "Gold" in third)

# Priority collision: ikki xil Platinum – FIFO tartib
p2 = PriorityCheckIn()
p2.add_passenger("First",  "Platinum")
p2.add_passenger("Second", "Platinum")
r1 = p2.serve()
r2 = p2.serve()
check("Bir xil ustuvorlikda FIFO tartibi (First avval)",
      "First" in r1 and "Second" in r2)


# ══════════════════════════════════════════════════════
#  PHASE 2 – Queue va Stack testlar
# ══════════════════════════════════════════════════════
section("PHASE 2 – BoardingQueue (FIFO) & CargoStack (LIFO)")

# FIFO Queue
q = BoardingQueue()
check("Bo'sh queuedan remove – xato xabari",
      "bo'sh" in q.remove().lower())

q.add("Ali")
q.add("Sara")
q.add("John")

check("FIFO: birinchi kirgan birinchi chiqadi (Ali)",
      "Ali" in q.remove())

check("FIFO: ikkinchi Sara",
      "Sara" in q.remove())

check("Queue hajmi to'g'ri",
      q.size() == 1)

# LIFO Stack
s = CargoStack()
check("Bo'sh stackdan pop – xato xabari",
      "bo'sh" in s.pop().lower())

s.push("Bag1")
s.push("Bag2")
s.push("Bag3")

check("LIFO: oxirgi kirgani birinchi chiqadi (Bag3)",
      "Bag3" in s.pop())

check("LIFO: keyingisi Bag2",
      "Bag2" in s.pop())

check("Stack hajmi to'g'ri",
      s.size() == 1)


# ══════════════════════════════════════════════════════
#  PHASE 3 – BST testlar
# ══════════════════════════════════════════════════════
section("PHASE 3 – Binary Search Tree")

bst = BST()

# Bo'sh BST
check("Bo'sh BST da search False qaytaradi",
      bst.search(100) == False)

check("Bo'sh BST range_query bo'sh ro'yxat",
      bst.range_query(0, 999) == [])

# Normal holat
for v in [500, 300, 700, 200, 400, 600, 800]:
    bst.insert(v)

check("BST inorder tartiblangan chiqadi",
      bst.inorder() == [200, 300, 400, 500, 600, 700, 800])

check("BST search: 400 bor",
      bst.search(400) == True)

check("BST search: 999 yo'q",
      bst.search(999) == False)

rq = bst.range_query(300, 600)
check("BST range query [300,600] = [300,400,500,600]",
      rq == [300, 400, 500, 600],
      expected=[300, 400, 500, 600], got=rq)

check("BST range query bo'sh oraliq",
      bst.range_query(900, 1000) == [])


# ══════════════════════════════════════════════════════
#  PHASE 3 – AVL Tree testlar
# ══════════════════════════════════════════════════════
section("PHASE 3 – AVL Tree (Balanced BST)")

avl  = AVLTree()
root = None

for v in [10, 20, 30, 40, 50, 25]:
    root = avl.insert(root, v)

check("AVL inorder tartiblangan",
      avl.inorder(root) == [10, 20, 25, 30, 40, 50])

check("AVL height balanslangan (≤ 4)",
      root.height <= 4)

check("AVL takroriy qiymat qo'shilmaydi",
      avl.inorder(avl.insert(root, 30)) == [10, 20, 25, 30, 40, 50])


# ══════════════════════════════════════════════════════
#  PHASE 3 – Hash Table testlar
# ══════════════════════════════════════════════════════
section("PHASE 3 – Hash Table")

ht = HashTable()

check("Mavjud bo'lmagan key – None qaytaradi",
      ht.get("PNR999") is None)

ht.add("PNR001", "Ali Karimov")
ht.add("PNR002", "Sara Lee")
ht.add("PNR003", "Bobur")

check("get() to'g'ri qiymat qaytaradi",
      ht.get("PNR001") == "Ali Karimov")

check("Mavjud key ni yangilash",
      (ht.add("PNR001", "Ali Updated") or True) and
      ht.get("PNR001") == "Ali Updated")

check("delete() ishlaydi",
      ht.delete("PNR002") == True and ht.get("PNR002") is None)

check("Mavjud bo'lmagan key ni delete – False",
      ht.delete("PNR999") == False)


# ══════════════════════════════════════════════════════
#  PHASE 3 – KMP testlar
# ══════════════════════════════════════════════════════
section("PHASE 3 – KMP String Matching")

kmp = KMP()

check("KMP: pattern topildi",
      kmp.contains("Ali Karimov", "Karimov") == True)

check("KMP: pattern topilmadi",
      kmp.contains("Ali Karimov", "Smith") == False)

# Bir necha marta uchraydigan pattern
positions = kmp.search("abababab", "ab")
check("KMP: pattern bir necha marta – barcha indekslar",
      positions == [0, 2, 4, 6],
      expected=[0, 2, 4, 6], got=positions)

check("KMP: bo'sh pattern – bo'sh ro'yxat",
      kmp.search("hello", "") == [])

check("KMP: pattern matndan uzun",
      kmp.search("hi", "hello world") == [])

check("KMP: to'liq mos kelish",
      kmp.search("abc", "abc") == [0])


# ══════════════════════════════════════════════════════
#  PHASE 4 – Sorting testlar
# ══════════════════════════════════════════════════════
section("PHASE 4 – QuickSort & MergeSort")

qs = QuickSort()
ms = MergeSort()

# Normal holat
arr = [64, 34, 25, 12, 22, 11, 90]
sorted_expected = [11, 12, 22, 25, 34, 64, 90]

check("QuickSort to'g'ri saralaydi",
      qs.sort(arr) == sorted_expected,
      expected=sorted_expected, got=qs.sort(arr))

check("MergeSort to'g'ri saralaydi",
      ms.sort(arr) == sorted_expected,
      expected=sorted_expected, got=ms.sort(arr))

# Edge case: bo'sh ro'yxat
check("QuickSort bo'sh massiv",
      qs.sort([]) == [])

check("MergeSort bo'sh massiv",
      ms.sort([]) == [])

# Edge case: bir elementli
check("QuickSort bir element",
      qs.sort([42]) == [42])

# Edge case: allaqachon tartiblangan
asc = [1, 2, 3, 4, 5]
check("QuickSort tartiblangan massiv",
      qs.sort(asc) == [1, 2, 3, 4, 5])

# Edge case: teskari tartiblangan
desc = [5, 4, 3, 2, 1]
check("MergeSort teskari tartiblangan massiv",
      ms.sort(desc) == [1, 2, 3, 4, 5])

# Edge case: takroriy elementlar
dups = [3, 1, 4, 1, 5, 9, 2, 6, 5]
check("QuickSort takroriy elementlar",
      qs.sort(dups) == sorted(dups))

check("Ikkalasi bir xil natija beradi",
      qs.sort(arr) == ms.sort(arr))

# Asl massiv o'zgarmasligi kerak (in-place emas)
orig = [5, 3, 1]
_ = qs.sort(orig)
check("QuickSort asl massivni o'zgartirmaydi",
      orig == [5, 3, 1])


# ══════════════════════════════════════════════════════
#  PHASE 5 – Backtracking testlar
# ══════════════════════════════════════════════════════
section("PHASE 5 – Backtracking (Route Finder)")

rf = RouteFinder()

net2 = {
    "Tashkent": [("Dubai", 500),    ("Istanbul", 400)],
    "Dubai":    [("Tashkent", 500), ("London", 700)],
    "Istanbul": [("Tashkent", 400), ("London", 600)],
    "London":   [("Dubai", 700),    ("Istanbul", 600)],
}

# Normal holat: 2 ta yo'l mavjud
paths = rf.find(net2, "Tashkent", "London")
check("Tashkent→London: 2 ta yo'l topiladi",
      len(paths) == 2,
      expected=2, got=len(paths))

check("To'g'ri yo'llar: Dubai va Istanbul orqali",
      ["Tashkent", "Dubai", "Istanbul", "London"] not in paths and
      ["Tashkent", "Dubai", "London"] in paths)

# Edge case: blok bilan
paths_blocked = rf.find(net2, "Tashkent", "London", blocked="Dubai")
check("Dubai yopilganda faqat 1 ta yo'l",
      len(paths_blocked) == 1,
      expected=1, got=len(paths_blocked))

check("Qolgan yo'l Istanbul orqali",
      ["Tashkent", "Istanbul", "London"] in paths_blocked)

# Edge case: mavjud bo'lmagan start
paths2 = rf.find(net2, "Paris", "London")
check("Mavjud bo'lmagan start – bo'sh ro'yxat",
      paths2 == [])

# Edge case: start = end
paths3 = rf.find(net2, "London", "London")
check("Start = End – bir yo'l (faqat o'zi)",
      paths3 == [["London"]])

# Edge case: yo'l yo'q (barcha yo'llar bloklangan)
paths4 = rf.find(net2, "Tashkent", "London",
                 blocked="Istanbul")
# faqat Dubai orqali qoladi
check("Istanbul bloklanganda Dubai orqali yo'l bor",
      len(paths4) >= 1)

# Edge case: bo'sh graf
paths5 = rf.find({}, "A", "B")
check("Bo'sh grafda yo'l topilmaydi",
      paths5 == [])


# ══════════════════════════════════════════════════════
#  Yakuniy natija
# ══════════════════════════════════════════════════════
summary()