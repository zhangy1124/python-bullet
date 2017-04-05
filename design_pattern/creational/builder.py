# -*- coding: utf-8 -*-

"""
Builder Pattern


Real world example

Imagine you are at Hardee's and you order a specific deal, lets say,
"Big Hardee" and they hand it over to you without any questions; this is the 
example of simple factory. But there are cases when the creation logic might 
involve more steps. For example you want a customized Subway deal, you have 
several options in how your burger is made e.g what bread do you want? what 
types of sauces would you like? What cheese would you want? etc. In such cases
builder pattern comes to the rescue.


In plain words

Allows you to create different flavors of an object while avoiding constructor
pollution. Useful when there could be several flavors of an object. Or when 
there are a lot of steps involved in creation of an object.


Wikipedia says

The builder pattern is an object creation software design pattern with the 
intentions of finding a solution to the telescoping constructor anti-pattern.
"""


class Pizza(object):
    def __init__(self):
        self.dough = ''
        self.sauce = ''
        self.topping = ''


class PizzaBuilder(object):
    def __init__(self):
        self.pizza = None

    def create_new_pizza(self):
        self.pizza = Pizza()

    def build_dough(self):
        raise NotImplementedError()

    def build_sauce(self):
        raise NotImplementedError()

    def build_topping(self):
        raise NotImplementedError()


class HawaiianPizzaBuilder(PizzaBuilder):
    def build_dough(self):
        self.pizza.dough = 'cross'

    def build_sauce(self):
        self.pizza.sauce = 'mild'

    def build_topping(self):
        self.pizza.topping = 'ham+pineapple'


class SpicyPizzaBuilder(PizzaBuilder):
    def build_dough(self):
        self.pizza.dough = 'pan baked'

    def build_sauce(self):
        self.pizza.sauce = 'hot'

    def build_topping(self):
        self.pizza.topping = 'pepperoni+salami'


class Waiter(object):
    def __init__(self):
        self.pizza_builder = None

    def contract_pizza(self):
        self.pizza_builder.create_new_pizza()
        self.pizza_builder.build_dough()
        self.pizza_builder.build_sauce()
        self.pizza_builder.build_topping()

    def get_pizza(self):
        return self.pizza_builder.pizza


# usage

waiter = Waiter()
hawaiian_pizza_builder = HawaiianPizzaBuilder()
spicy_pizza_builder = SpicyPizzaBuilder()

waiter.pizza_builder = hawaiian_pizza_builder
waiter.contract_pizza()

pizza = waiter.get_pizza()
