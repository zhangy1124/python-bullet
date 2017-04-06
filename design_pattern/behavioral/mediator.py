# -*- coding: utf-8 -*-

"""
Mediator Pattern


Real world example

A general example would be when you talk to someone on your mobile phone, 
there is a network provider sitting between you and them and your 
conversation goes through it instead of being directly sent. In this case 
network provider is mediator.


In plain words

Mediator pattern adds a third party object (called mediator) to control the 
interaction between two objects (called colleagues). It helps reduce the 
coupling between the classes communicating with each other. Because now they 
don't need to have the knowledge of each other's implementation.


Wikipedia says

In software engineering, the mediator pattern defines an object that 
encapsulates how a set of objects interact. This pattern is considered to be 
a behavioral pattern due to the way it can alter the program's running 
behavior.
"""


import time


class ChatRoom(object):
    def show_message(self, name, message):
        print('{} [{}]: {}'.format(time.ctime(), name, message))


class User(object):
    def __init__(self, name, mediator):
        self.name = name
        self.mediator = mediator

    def send(self, message):
        self.mediator.show_message(self.name, message)


# usage

mediator = ChatRoom()

john = User('join', mediator)
alice = User('alice', mediator)

john.send("hey, what's up")
alice.send("hey!")

