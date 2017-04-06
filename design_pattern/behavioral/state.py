# -*- coding: utf-8 -*-


"""
State Pattern


Real world example

Imagine you are using some drawing application, you choose the paint brush 
to draw. Now the brush changes its behavior based on the selected color i.e. 
if you have chosen red color it will draw in red, if blue then it will be in 
blue etc.


In plain words

It lets you change the behavior of a class when the state changes.


Wikipedia says

The state pattern is a behavioral software design pattern that implements a 
state machine in an object-oriented way. With the state pattern, a state 
machine is implemented by implementing each individual state as a derived 
class of the state pattern interface, and implementing state transitions by 
invoking methods defined by the pattern's superclass. The state pattern can 
be interpreted as a strategy pattern which is able to switch the current 
strategy through invocations of methods defined in the pattern's interface.
"""


URGENCY_FLAG = False

DOWNGRADE_POOL = {}


def downgrade_service(func):
    if func.__name__.endswith('_downgrade'):
        DOWNGRADE_POOL[func.__name__[:-10]] = func
        downgrade = True
    else:
        downgrade = False

    def wrapper(*args, **kwargs):
        if downgrade or not URGENCY_FLAG:
            return func(*args, **kwargs)
        else:
            return DOWNGRADE_POOL[func.__name__](*args, **kwargs)
    return wrapper


@downgrade_service
def foo(payload):
    print('Give what you want ' + payload.upper())


@downgrade_service
def foo_downgrade(payload):
    print('421 service temporarily unavailable for ' + payload.upper())


# usage

foo('google')

URGENCY_FLAG = True

foo('google')
