# -*- coding: utf-8 -*-

"""
Adapter pattern


Real world example

Consider that you have some pictures in your memory card and you need to 
transfer them to your computer. In order to transfer them you need some kind 
of adapter that is compatible with your computer ports so that you can attach 
memory card to your computer. In this case card reader is an adapter. Another 
example would be the famous power adapter; a three legged plug can't be 
connected to a two pronged outlet, it needs to use a power adapter that makes
it compatible with the two pronged outlet. Yet another example would be a 
translator translating words spoken by one person to another


In plain words

Adapter pattern lets you wrap an otherwise incompatible object in an adapter 
to make it compatible with another class.


Wikipedia says

In software engineering, the adapter pattern is a software design pattern 
that allows the interface of an existing class to be used as another 
interface. It is often used to make existing classes work with others 
without modifying their source code.
"""


class TwoEndSocket(object):
    def charge(self):
        pass


class Hotel(object):
    def charge(self, charge_socket):
        return charge_socket.charge()


class ThreeSocket(object):
    def specific_charge(self):
        pass


class ThreeEndSocketAdapter(object):
    def __init__(self):
        self.charge_socket = ThreeSocket()

    def charge(self):
        self.charge_socket.specific_charge()


# usage

hotel = Hotel()
hotel.charge(TwoEndSocket())
hotel.charge(ThreeEndSocketAdapter())
