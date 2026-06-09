import heapq
from collections import deque


class PriorityCheckIn:
    def __init__(self):
        self.heap = []

    def add_passenger(self, name, level):
        # ustuvorlik darajasi
        if level == "Platinum":
            p = 3
        elif level == "Gold":
            p = 2
        else:
            p = 1

        heapq.heappush(self.heap, (-p, name, level))

    def serve(self):
        if not self.heap:
            return "Yo‘lovchi yo‘q"

        return heapq.heappop(self.heap)


class BoardingQueue:
    def __init__(self):
        self.queue = deque()

    def add(self, p):
        self.queue.append(p)

    def remove(self):
        if not self.queue:
            return "Bo'sh"

        return self.queue.popleft()


class CargoStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.stack:
            return "Bo'sh"
        return self.stack.pop()