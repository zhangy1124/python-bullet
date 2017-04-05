# -*- coding: utf-8 -*-

"""
Bridge Pattern


Real world example

Consider you have a website with different pages and you are supposed to 
allow the user to change the theme. What would you do? Create multiple 
copies of each of the pages for each of the themes or would you just create 
separate theme and load them based on the user's preferences? Bridge pattern 
allows you to do the second i.e.


In Plain Words

Bridge pattern is about preferring composition over inheritance. 
Implementation details are pushed from a hierarchy to another object with a 
separate hierarchy.


Wikipedia says

The bridge pattern is a design pattern used in software engineering that is 
meant to "decouple an abstraction from its implementation so that the two 
can vary independently"
"""


class Drawing(object):
    def drawing_circle(self, x, y, radius):
        raise NotImplementedError()


class RedDrawing(Drawing):
    def drawing_circle(self, x, y, radius):
        print('Drawing red circle in {} / {} / {}'.format(x, y, radius))


class GreenDrawing(Drawing):
    def drawing_circle(self, x, y, radius):
        print('Drawing green circle in {} / {} / {}'.format(x, y, radius))


class Shape(object):
    def draw(self, *args, **kwargs):
        raise NotImplementedError()


class CircleShape(Shape):
    @staticmethod
    def draw(x, y, radius, drawing_method):
        drawing_method.drawing_circle(x, y, radius)


# usage

CircleShape.draw(1, 2, 3, RedDrawing())
