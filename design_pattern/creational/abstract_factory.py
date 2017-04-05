# -*- coding: utf-8 -*-

import sys


# Products
class Button(object):
    pass


class MacButton(Button):
    pass


class WinButton(Button):
    pass


class Border(object):
    pass


class MacBorder(Border):
    pass


class WinBorder(Border):
    pass


# Factories
class AbstractFactory(object):
    def __init__(self):
        self.factory = None

    def use_factory(self, factory):
        self.factory = factory

    def create_button(self):
        return self.factory.create_button()

    def create_border(self):
        return self.factory.create_border()


class MacFactory(object):
    def create_button(self):
        return MacButton()

    def create_border(self):
        return MacBorder()


class WinFactory(object):
    def create_button(self):
        return WinButton()

    def create_border(self):
        return WinBorder()


# client usage
client = AbstractFactory()

if sys.platform == 'win32':
    factory = WinFactory()
else:
    factory = MacFactory()

client.use_factory(factory)

client.create_button()
client.create_border()
