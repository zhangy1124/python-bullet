# -*- coding: utf-8 -*-


"""
Facade Pattern

Real world example

How do you turn on the computer? "Hit the power button" you say! That is 
what you believe because you are using a simple interface that computer 
provides on the outside, internally it has to do a lot of stuff to make it 
happen. This simple interface to the complex subsystem is a facade.


In plain words

Facade pattern provides a simplified interface to a complex subsystem.


Wikipedia says

A facade is an object that provides a simplified interface to a larger body 
of code, such as a class library.
"""


class Computer(object):
    def post(self):
        print('Power On Self Test')

    def read_mbr(self):
        print('read mbr')

    def start_hard_drive(self):
        print('start hard drive')

    def start_os(self):
        print('start operating system')

    def close_all_process(self):
        print('close all process')

    def close_os(self):
        print('close operating system')

    def close_power(self):
        print('close power')


class FacadeComputer(object):
    def __init__(self, computer):
        self.computer = computer

    def power_on(self):
        self.computer.post()
        self.computer.read_mbr()
        self.computer.start_hard_drive()
        self.computer.start_os()

    def power_off(self):
        self.computer.close_all_process()
        self.computer.close_os()
        self.computer.close_power()


# usage

computer = FacadeComputer(Computer())
computer.power_on()
computer.power_off()
