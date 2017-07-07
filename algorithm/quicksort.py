# -*- coding: utf-8 -*-

def quicksort(data):
    less = []
    equal = []
    greater = []

    if len(data) > 1:
        pivot = data[0]
        for x in data:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            else:
                greater.append(x)
        return quicksort(less) + equal + quicksort(greater)
    else:
        return data

print(quicksort([1,2,3,4,5,6,100,0]))
