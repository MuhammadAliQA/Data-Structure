class QuickSort:
    def sort(self, arr):
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr)//2]

        left = [x for x in arr if x < pivot]
        mid = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        return self.sort(left) + mid + self.sort(right)


class MergeSort:
    def sort(self, arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr)//2

        left = self.sort(arr[:mid])
        right = self.sort(arr[mid:])

        return self.merge(left, right)

    def merge(self, l, r):
        res = []
        i = j = 0

        while i < len(l) and j < len(r):
            if l[i] < r[j]:
                res.append(l[i])
                i += 1
            else:
                res.append(r[j])
                j += 1

        res += l[i:]
        res += r[j:]

        return res