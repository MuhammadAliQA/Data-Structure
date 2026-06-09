from graph import Graph, Dijkstra, Kruskal
from passenger import PriorityCheckIn, BoardingQueue, CargoStack
from search import BST, HashTable, KMP
from sorting import QuickSort, MergeSort
from routing import RouteFinder


g = Graph()
d = Dijkstra()
k = Kruskal()

check = PriorityCheckIn()
queue = BoardingQueue()
cargo = CargoStack()

bst = BST()
ht = HashTable()
kmp = KMP()

rf = RouteFinder()


def setup():
    g.add_airport("Tashkent")
    g.add_airport("Dubai")
    g.add_airport("Istanbul")
    g.add_airport("London")

    g.add_flight("Tashkent", "Dubai", 500)
    g.add_flight("Tashkent", "Istanbul", 400)
    g.add_flight("Dubai", "London", 700)
    g.add_flight("Istanbul", "London", 600)


setup()


while True:
    print("\n1. Graph")
    print("2. Dijkstra")
    print("3. MST")
    print("4. Priority")
    print("5. Queue & Stack")
    print("6. Search")
    print("7. Sort")
    print("8. Routes")
    print("0. Exit")

    c = input("Tanlang: ")

    if c == "1":
        g.display()

    elif c == "2":
        print(d.shortest_path(g.graph, "Tashkent"))

    elif c == "3":
        print(k.mst(g.graph))

    elif c == "4":
        check.add_passenger("Ali", "Platinum")
        check.add_passenger("John", "Gold")
        print(check.serve())

    elif c == "5":
        queue.add("Ali")
        cargo.push("Bag")
        print(queue.remove())
        print(cargo.pop())

    elif c == "6":
        ht.add("PNR1", "Ali")
        print(ht.get("PNR1"))
        print(kmp.search("Ali Airport", "Ali"))

    elif c == "7":
        q = QuickSort()
        print(q.sort([5,2,9,1]))

    elif c == "8":
        print(rf.find(g.graph, "Tashkent", "London"))

    elif c == "0":
        break