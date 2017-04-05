# -*- coding: utf-8 -*-

"""
Prototype Pattern


Real world example

Remember dolly? The sheep that was cloned! Lets not get into the details but
the key point here is that it is all about cloning


In plain words

Create object based on an existing object through cloning.


Wikipedia says

The prototype pattern is a creational design pattern in software development.
It is used when the type of objects to create is determined by a prototypical
instance, which is cloned to produce new objects.
"""

import copy


class Prototype(object):
    pass


# usage

a = Prototype()
a.name = 'a'

b = copy.deepcopy(a)
print(b.name)
b.name = 'b'
print(b.name)
