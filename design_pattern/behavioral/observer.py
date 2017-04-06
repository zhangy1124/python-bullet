# -*- coding: utf-8 -*-

"""
Observer Pattern


Real world example

A good example would be the job seekers where they subscribe to some job 
posting site and they are notified whenever there is a matching job 
opportunity.


In plain words

Defines a dependency between objects so that whenever an object changes its 
state, all its dependents are notified.


Wikipedia says

The observer pattern is a software design pattern in which an object, 
called the subject, maintains a list of its dependents, called observers, 
and notifies them automatically of any state changes, usually by calling one 
of their methods.
"""


class Observable(object):
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.notify(message)


class Observer(object):
    def __init__(self, observerable):
        self.observerable = observerable
        observerable.register_observer(self)

    def notify(self, message):
        print("Got {} from {}".format(message, self.observerable.__class__.__name__))


# usage

subject = Observable()
observer = Observer(subject)
subject.notify_observers('nice to meet you')

