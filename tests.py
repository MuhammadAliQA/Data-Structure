from graph import Graph, Dijkstra, Kruskal
from passenger import PriorityCheckIn, BoardingQueue, CargoStack
from search import BST, HashTable, KMP
from sorting import QuickSort, MergeSort
from routing import RouteFinder


# oddiy test qilish uchun
print("\n===== TESTLAR BOSHLANDI =====\n")


# ---------------- GRAPH ----------------
print("GRAPH TEST")

g = Graph()
g.add_airport("A")
g.add_airport("B")
g.add_flight("A", "B", 10)

g.display()


# ---------------- DIJKSTRA ----------------
print("\nDIJKSTRA TEST")

graph_data = {
    "A": [("B", 5), ("C", 2)],
    "B": [("C", 1)],
    "C": []
}

d = Dijkstra()
print(d.shortest_path(graph_data, "A"))


# ---------------- MST ----------------
print("\nMST TEST")

graph_mst = {
    "A": [("B", 1), ("C", 4)],
    "B": [("A", 1), ("C", 2)],
    "C": [("A", 4), ("B", 2)]
}

k = Kruskal()
print(k.mst(graph_mst))


# ---------------- PRIORITY ----------------
print("\nPRIORITY TEST")

p = PriorityCheckIn()

p.add_passenger("Ali", "Platinum")
p.add_passenger("John", "Gold")
p.add_passenger("Sara", "Economy")

print(p.serve())


# ---------------- QUEUE + STACK ----------------
print("\nQUEUE & STACK TEST")

q = BoardingQueue()
s = CargoStack()

q.add("Ali")
q.add("John")

s.push("Bag1")
s.push("Bag2")

print(q.remove())
print(s.pop())


# ---------------- SEARCH ----------------
print("\nSEARCH TEST")

bst = BST()
ht = HashTable()
kmp = KMP()

ht.add("PNR1", "Ali")

print(ht.get("PNR1"))
print(kmp.search("Ali Airport", "Ali"))


# ---------------- SORTING ----------------
print("\nSORTING TEST")

qsort = QuickSort()
msort = MergeSort()

arr = [9, 1, 5, 3]

print(qsort.sort(arr))
print(msort.sort(arr))


# ---------------- ROUTES ----------------
print("\nROUTE TEST")

graph_r = {
    "A": [("B", 1), ("C", 1)],
    "B": [("D", 1)],
    "C": [("D", 1)],
    "D": []
}

r = RouteFinder()
print(r.find(graph_r, "A", "D"))


print("\n===== TESTLAR TUGADI =====")