import time


# ══════════════════════════════════════════════
#  QUICKSORT
#  Best / Average : O(n log n)
#  Worst          : O(n²)  – avoided with median-of-three pivot
#  Space          : O(log n) call stack
#  In-place, NOT stable
# ══════════════════════════════════════════════
class QuickSort:
    """
    QuickSort with median-of-three pivot selection to avoid O(n²)
    on already-sorted or reverse-sorted flight schedules.
    """

    def sort(self, arr: list) -> list:
        data = arr[:]          # work on a copy – don't mutate original
        self._quick(data, 0, len(data) - 1)
        return data

    def _quick(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)
            self._quick(arr, low,    pi - 1)
            self._quick(arr, pi + 1, high)

    def _partition(self, arr, low, high):
        # ── Median-of-three pivot ──
        mid = (low + high) // 2
        # sort arr[low], arr[mid], arr[high] so median ends up at arr[high]
        if arr[mid] < arr[low]:
            arr[low], arr[mid] = arr[mid], arr[low]
        if arr[high] < arr[low]:
            arr[low], arr[high] = arr[high], arr[low]
        if arr[mid] < arr[high]:
            arr[mid], arr[high] = arr[high], arr[mid]

        pivot = arr[high]
        i     = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1


# ══════════════════════════════════════════════
#  MERGESORT
#  Best / Average / Worst : O(n log n)  always
#  Space                  : O(n)  auxiliary
#  Stable sort
# ══════════════════════════════════════════════
class MergeSort:
    """
    MergeSort guarantees O(n log n) in ALL cases.
    Preferred when stability matters (e.g. preserving relative order
    of flights with equal departure times).
    """

    def sort(self, arr: list) -> list:
        if len(arr) <= 1:
            return arr[:]
        mid   = len(arr) // 2
        left  = self.sort(arr[:mid])
        right = self.sort(arr[mid:])
        return self._merge(left, right)

    def _merge(self, left, right) -> list:
        result = []
        i = j  = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i]);  i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result


# ══════════════════════════════════════════════
#  COMPARISON UTILITY
# ══════════════════════════════════════════════
def compare_sorts(data: list) -> dict:
    """
    Run QuickSort and MergeSort on the same dataset and report:
      - sorted result (both should be identical)
      - elapsed time in microseconds

    Returns a dict with keys: quick_result, merge_result,
                               quick_time_us, merge_time_us, winner
    """
    qs = QuickSort()
    ms = MergeSort()

    t0       = time.perf_counter()
    res_q    = qs.sort(data)
    time_q   = (time.perf_counter() - t0) * 1_000_000   # µs

    t0       = time.perf_counter()
    res_m    = ms.sort(data)
    time_m   = (time.perf_counter() - t0) * 1_000_000

    winner = "QuickSort" if time_q <= time_m else "MergeSort"

    return {
        "quick_result":  res_q,
        "merge_result":  res_m,
        "quick_time_us": round(time_q, 3),
        "merge_time_us": round(time_m, 3),
        "winner":        winner,
    }