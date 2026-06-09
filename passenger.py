import heapq
from collections import deque


class PriorityCheckIn:
    """
    Max-Heap asosida Priority Queue.
    Yo'lovchilar ticket statusiga ko'ra tartiblanadi:
      Platinum = 3 (eng yuqori), Gold = 2, Economy = 1
    """

    LEVELS = {"Platinum": 3, "Gold": 2, "Economy": 1}

    def __init__(self):
        self.heap    = []
        self._counter = 0          # bir xil ustuvorlikda FIFO tartibini saqlash uchun

    def add_passenger(self, name, level):
        priority = self.LEVELS.get(level, 1)
        # heapq min-heap bo'lgani uchun manfiy qilamiz
        heapq.heappush(self.heap, (-priority, self._counter, name, level))
        self._counter += 1
        print(f"  + {name} ({level}) navbatga qo'shildi.")

    def serve(self):
        if not self.heap:
            return "  Navbat bo'sh – xizmat qilinadigan yo'lovchi yo'q."
        _, _, name, level = heapq.heappop(self.heap)
        return f"  ✓ Xizmat ko'rsatildi: {name} [{level}]"

    def peek(self):
        if not self.heap:
            return "  Navbat bo'sh."
        _, _, name, level = self.heap[0]
        return f"  Keyingi: {name} [{level}]"

    def size(self):
        return len(self.heap)


# ─────────────────────────────────────────────────────
class BoardingQueue:
    """
    FIFO Queue – boarding gate uchun.
    Birinchi kelgan yo'lovchi birinchi chiqadi.
    """

    def __init__(self):
        self.queue = deque()

    def add(self, passenger):
        self.queue.append(passenger)
        print(f"  + {passenger} boarding navbatiga qo'shildi.")

    def remove(self):
        if not self.queue:
            return "  Boarding navbati bo'sh."
        passenger = self.queue.popleft()
        return f"  ✓ Boarding: {passenger} samolyotga kirdi."

    def size(self):
        return len(self.queue)


# ─────────────────────────────────────────────────────
class CargoStack:
    """
    LIFO Stack – yuk ombori (cargo hold) uchun.
    Oxirgi yuklangan yuk birinchi tushiriladi.
    """

    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)
        print(f"  + '{item}' yukxonaga joylashtirildi.")

    def pop(self):
        if not self.stack:
            return "  Yukxona bo'sh."
        item = self.stack.pop()
        return f"  ✓ Yukxonadan chiqarildi: '{item}'"

    def peek(self):
        if not self.stack:
            return "  Yukxona bo'sh."
        return f"  Tepada: '{self.stack[-1]}'"

    def size(self):
        return len(self.stack)