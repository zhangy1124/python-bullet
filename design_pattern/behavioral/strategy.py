# -*- coding: utf-8 -*-

"""
Strategy Pattern


Real world example

Consider the example of sorting, we implemented bubble sort but the data 
started to grow and bubble sort started getting very slow. In order to 
tackle this we implemented Quick sort. But now although the quick sort 
algorithm was doing better for large datasets, it was very slow for smaller 
datasets. In order to handle this we implemented a strategy where for small 
datasets, bubble sort will be used and for larger, quick sort.


In plain words

Strategy pattern allows you to switch the algorithm or strategy based upon 
the situation.


Wikipedia says

In computer programming, the strategy pattern (also known as the policy 
pattern) is a behavioural software design pattern that enables an 
algorithm's behavior to be selected at runtime.
"""


class SortStrategy(object):
    def sort(self, data):
        raise NotImplementedError()


class BubbleSortStrategy(SortStrategy):
    def sort(self, data):
        print('Sorting using bubble sort')
        return data


class QuickSortStrategy(SortStrategy):
    def sort(self, data):
        print('Sorting using quick sort')
        return data


class Sorter(object):
    def __init__(self, strategy):
        self.strategy = strategy

    def sort(self, data):
        return self.strategy.sort(data)


# usage

data = [1, 5, 3, 4, 2]
sorter1 = Sorter(BubbleSortStrategy())
sorter2 = Sorter(QuickSortStrategy())

sorter1.sort(data)
sorter2.sort(data)
