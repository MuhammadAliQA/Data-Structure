import heapq
from collections import deque


# ══════════════════════════════════════════════
#  PRIORITY CHECK-IN  –  Max-Heap (Priority Queue)
#  ADT: PriorityQueue
#  push : O(log n)
#  pop  : O(log n)
#  peek : O(1)
# ══════════════════════════════════════════════

TICKET_RANK = {
    "Platinum": 3,
    "Gold":     2,
    "Silver":   1,
    "Economy":  0,
}


class PriorityCheckIn:
    """
    Passengers are served by ticket class (Platinum > Gold > Silver > Economy).
    Ties are broken by arrival order (FIFO within same class).

    Internal representation: min-heap with negated priority so the
    highest-priority passenger is always at the top.
    """

    def __init__(self):
        self._heap    = []      # ( -priority, arrival_order, name, ticket_class )
        self._counter = 0       # arrival order counter

    # ---------- public interface ----------

    def add_passenger(self, name: str, ticket_class: str) -> None:
        if not name.strip():
            raise ValueError("Passenger name cannot be empty.")
        if ticket_class not in TICKET_RANK:
            raise ValueError(
                f"Unknown ticket class '{ticket_class}'. "
                f"Valid: {list(TICKET_RANK.keys())}"
            )
        priority = TICKET_RANK[ticket_class]
        heapq.heappush(self._heap, (-priority, self._counter, name, ticket_class))
        self._counter += 1

    def serve(self) -> dict | str:
        """Remove and return the highest-priority passenger."""
        if self.is_empty():
            return "Check-in queue is empty – no passengers waiting."
        _, _, name, ticket_class = heapq.heappop(self._heap)
        return {"name": name, "class": ticket_class}

    def peek(self) -> dict | str:
        """View next passenger without removing."""
        if self.is_empty():
            return "Queue is empty."
        _, _, name, ticket_class = self._heap[0]
        return {"name": name, "class": ticket_class}

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)


# ══════════════════════════════════════════════
#  BOARDING GATE QUEUE  –  FIFO (Standard Queue)
#  ADT: Queue
#  enqueue : O(1)
#  dequeue : O(1)
# ══════════════════════════════════════════════
class BoardingQueue:
    """
    Standard FIFO queue for passengers boarding the aircraft.
    First passenger to join the queue is first to board.
    """

    def __init__(self):
        self._queue = deque()

    def add(self, passenger: str) -> None:
        if not passenger.strip():
            raise ValueError("Passenger name cannot be empty.")
        self._queue.append(passenger)

    def remove(self) -> str:
        if self.is_empty():
            return "Boarding gate queue is empty."
        return self._queue.popleft()

    def peek(self) -> str:
        if self.is_empty():
            return "Queue is empty."
        return self._queue[0]

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def size(self) -> int:
        return len(self._queue)

    def display(self) -> None:
        if self.is_empty():
            print("  [Boarding queue is empty]")
        else:
            print("  Boarding order:", " → ".join(self._queue))


# ══════════════════════════════════════════════
#  CARGO HOLD STACK  –  LIFO (Stack)
#  ADT: Stack
#  push : O(1)
#  pop  : O(1)
#  peek : O(1)
# ══════════════════════════════════════════════
class CargoStack:
    """
    LIFO stack simulating a cargo hold.
    Last bag loaded is the first to be unloaded.
    """

    def __init__(self):
        self._stack = []

    def push(self, item: str) -> None:
        if not item.strip():
            raise ValueError("Cargo item name cannot be empty.")
        self._stack.append(item)

    def pop(self) -> str:
        if self.is_empty():
            return "Cargo hold is empty – nothing to unload."
        return self._stack.pop()

    def peek(self) -> str:
        if self.is_empty():
            return "Stack is empty."
        return self._stack[-1]

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def size(self) -> int:
        return len(self._stack)

    def display(self) -> None:
        if self.is_empty():
            print("  [Cargo hold is empty]")
        else:
            print("  Cargo hold (top → bottom):", " | ".join(reversed(self._stack)))