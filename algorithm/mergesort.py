# -*- coding: utf-8 -*-

from collections import deque

def mergesort(data):
    if len(data) <= 1:
        return data

    def merge(left, right):
        merged, left, right = deque(), deque(left), deque(right)
        while left and right:
            if left[0] < right[0]:
                merged.append(left.popleft())
            else:
                merged.append(right.popleft())
        merged.extend(left if left else right)
        return list(merged)

    middle = len(data) // 2
    left = mergesort(data[:middle])
    right = mergesort(data[middle:])
    return merge(left, right)


print(mergesort([1,2,3,45,6,6,7,90,100,0]))


