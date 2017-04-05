# -*- coding: utf-8 -*-

"""
Simple Factory Pattern

Real world example

Consider, you are building a house and you need doors. 
It would be a mess if every time you need a door, you put on your carpenter 
clothes and start making a door in your house. Instead you get it made from 
a factory.

In plain words

Simple factory simply generates an instance for client without exposing any 
instantiation logic to the client

Wikipedia says

In object-oriented programming (OOP), a factory is an object for creating 
other objects – formally a factory is a function or method that returns 
objects of a varying prototype or class from some method call, which is 
assumed to be "new".

When to Use?

When creating an object is not just a few assignments and involves some logic,
it makes sense to put it in a dedicated factory instead of repeating the same 
code everywhere.
"""


class Door(object):
    def height(self):
        raise NotImplementedError()

    def width(self):
        raise NotImplementedError()


class WoodenDoor(Door):
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def height(self):
        return self.height

    def width(self):
        return self.width


class DoorFactory(object):
    @staticmethod
    def make_door(height, width):
        return WoodenDoor(height, width)


# usage

door = DoorFactory.make_door(100, 200)
