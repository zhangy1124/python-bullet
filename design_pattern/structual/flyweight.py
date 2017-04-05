# -*- coding: utf-8 -*-

"""
Flyweight Pattern


Real world example

Did you ever have fresh tea from some stall? They often make more than one 
cup that you demanded and save the rest for any other customer so to save 
the resources e.g. gas etc. Flyweight pattern is all about that i.e. sharing.


In plain words

It is used to minimize memory usage or computational expenses by sharing as 
much as possible with similar objects.


Wikipedia says

In computer programming, flyweight is a software design pattern. A flyweight 
is an object that minimizes memory use by sharing as much data as possible 
with other similar objects; it is a way to use objects in large numbers when 
a simple repeated representation would use an unacceptable amount of memory.
"""


import weakref


class Client(object):
    instance_pool = weakref.WeakValueDictionary()

    def __new__(cls, name):
        if name in cls.instance_pool:
            return cls.instance_pool[name]
        else:
            return super(Client, cls).__new__(cls)

    def __init__(self, name):
        self.name = name
        self.instance_pool[name] = self


# usage

a = Client('a')
b = Client('a')


print(a.name)
print(b.name)
print(id(a) == id(b))

del a
del b

print(list(Client.instance_pool.items()))
