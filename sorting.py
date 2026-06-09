import time


# ─────────────────────────────────────────────────────
class QuickSort:
    """
    QuickSort – O(n log n) o'rtacha, O(n²) eng yomon holat.
    Pivot: o'rtadagi element (median-of-three yondashuvi).
    In-place saralash, qo'shimcha xotira talab qilmaydi.
    """

    def sort(self, arr):
        data = arr[:]
        self._quick(data, 0, len(data) - 1)
        return data

    def _quick(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)
            self._quick(arr, low, pi - 1)
            self._quick(arr, pi + 1, high)

    def _partition(self, arr, low, high):
        # median-of-three pivot tanlash
        mid = (low + high) // 2
        if arr[mid] < arr[low]:
            arr[low], arr[mid] = arr[mid], arr[low]
        if arr[high] < arr[low]:
            arr[low], arr[high] = arr[high], arr[low]
        if arr[mid] < arr[high]:
            arr[mid], arr[high] = arr[high], arr[mid]
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1


# ─────────────────────────────────────────────────────
class MergeSort:
    """
    MergeSort – O(n log n) har doim (worst/avg/best).
    Barqaror (stable) saralash, lekin O(n) qo'shimcha xotira kerak.
    """

    def sort(self, arr):
        if len(arr) <= 1:
            return arr[:]
        mid   = len(arr) // 2
        left  = self.sort(arr[:mid])
        right = self.sort(arr[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        result = []
        i = j  = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result


# ─────────────────────────────────────────────────────
def compare_sorts(data):
    """
    QuickSort va MergeSort ni bir xil ma'lumot bilan solishtiradi.
    Vaqt va natijani ko'rsatadi.
    """
    qs = QuickSort()
    ms = MergeSort()

    t0     = time.perf_counter()
    res_q  = qs.sort(data)
    time_q = (time.perf_counter() - t0) * 1_000_000   # mikrosaniya

    t0     = time.perf_counter()
    res_m  = ms.sort(data)
    time_m = (time.perf_counter() - t0) * 1_000_000

    return res_q, res_m, time_q, time_m