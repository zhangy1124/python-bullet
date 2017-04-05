# -*- coding: utf-8 -*-

"""
Decorator Pattern


Real world example

Imagine you run a car service shop offering multiple services. Now how do 
you calculate the bill to be charged? You pick one service and dynamically 
keep adding to it the prices for the provided services till you get the 
final cost. Here each type of service is a decorator.


In plain words

Decorator pattern lets you dynamically change the behavior of an object at 
run time by wrapping them in an object of a decorator class.


Wikipedia says

In object-oriented programming, the decorator pattern is a design pattern 
that allows behavior to be added to an individual object, either statically 
or dynamically, without affecting the behavior of other objects from the 
same class. The decorator pattern is often useful for adhering to the Single 
Responsibility Principle, as it allows functionality to be divided between 
classes with unique areas of concern.
"""


def text_tag(text):
    return text


def bold(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        return '<b>{}</b>'.format(text)
    return wrapper


def italic(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        return '<i>{}</i>'.format(text)
    return wrapper


bold_text = bold(text_tag)
italic_text = italic(text_tag)
bold_italic_text = bold(italic(text_tag))


# usage

welcome = text_tag('hello, world')
welcome_with_style = bold_italic_text(welcome)

print(welcome)
print(welcome_with_style)
