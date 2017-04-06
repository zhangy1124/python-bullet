# -*- coding: utf-8 -*-

"""
Chain of Responsibility


Real world example

For example, you have three payment methods (A, B and C) setup in your 
account; each having a different amount in it. A has 100 USD, B has 300 USD 
and C having 1000 USD and the preference for payments is chosen as A then B 
then C. You try to purchase something that is worth 210 USD. Using Chain of 
Responsibility, first of all account A will be checked if it can make the 
purchase, if yes purchase will be made and the chain will be broken. If not, 
request will move forward to account B checking for amount if yes chain will 
be broken otherwise the request will keep forwarding till it finds the 
suitable handler. Here A, B and C are links of the chain and the whole 
phenomenon is Chain of Responsibility.


In plain words

It helps building a chain of objects. Request enters from one end and keeps 
going from object to object till it finds the suitable handler.


Wikipedia says

In object-oriented design, the chain-of-responsibility pattern is a design 
pattern consisting of a source of command objects and a series of processing 
objects. Each processing object contains logic that defines the types of 
command objects that it can handle; the rest are passed to the next 
processing object in the chain.
"""


class Account(object):
    def __init__(self, balance):
        self.successor = None
        self.balance = balance

    def set_successor(self, successor):
        self.successor = successor

    def pay(self, amount):
        if self.balance > amount:
            print('Paid {} using {}'.format(amount, self.__class__.__name__))
        elif self.successor:
            print('Cannot pay using' + self.__class__.__name__)
            self.successor.pay(amount)
        else:
            raise ValueError('None of the accounts have enough balance')


class Bank(Account):
    pass


class Paypal(Account):
    pass


class Bitcoin(Account):
    pass


# usage

bank = Bank(100)
paypal = Paypal(200)
bitcoin = Bitcoin(300)

bank.set_successor(paypal)
paypal.set_successor(bitcoin)

bank.pay(249)
