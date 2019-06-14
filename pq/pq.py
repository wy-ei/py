# -*- coding: utf-8 -*-

import heapq

__all__ = ["MaxPQ"]


class HeapObj:
    def __init__(self, val, key):
        self.val = val
        self.key = key

    def __eq__(self, other):
        return self.key(self.val) == self.key(other.val)

    def __str__(self):
        return str(self.key(self.val))


class MaxHeapObj(HeapObj):
    def __lt__(self, other):
        return self.key(self.val) < self.key(other.val)


class MaxPQ:
    def __init__(self, max_size=None, key=lambda x: x):
        self.heap = []
        self.key = key

        if max_size is None:
            self.max_size = 9999999
        else:
            self.max_size = max_size

    def add(self, item):
        if len(self.heap) == self.max_size:
            heapq.heappush(self.heap, MaxHeapObj(item, self.key))
            heapq.heappop(self.heap)
        else:
            heapq.heappush(self.heap, MaxHeapObj(item, self.key))

    def __len__(self):
        return len(self.heap)

    def __getitem__(self, i):
        return self.heap[i].val

    def values(self):
        items = sorted(self.heap, reverse=True)
        ret = [item.val for item in items]
        return ret


if __name__ == '__main__':
    import random

    max_pq = MaxPQ(max_size=5, key=lambda x: x['n'])
    for _ in range(100):
        max_pq.add({
            'n': random.randint(0, 10000)
        })

    print(max_pq.values())
