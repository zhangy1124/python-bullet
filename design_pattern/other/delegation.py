# -*- coding: utf-8 -*-

"""
Delegation Pattern


In delegation, an object handles a request by delegating to a second object 
(the delegate). The delegate is a helper object, but with the original 
context. With language-level support for delegation, this is done implicitly 
by having self in the delegate refer to the original (sending) object, 
not the delegate (receiving object). In the delegate pattern, this is 
instead accomplished by explicitly passing the original object to the 
delegate, as an argument to a method.[1] Note that "delegation" is often 
used loosely to refer to the distinct concept of forwarding, where the 
sending object simply uses the corresponding member on the receiving object, 
evaluated in the context of the receiving object, not the original object.
"""


class Delegator(object):
    def __init__(self, target):
        self.target =  target

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            if hasattr(self.target, name):
                attr = getattr(self.target, name)
                if callable(attr):
                    return attr(*args, **kwargs)
        return wrapper


class Target(object):
    def do_something(self, something):
        print('Doing ' + something)


# usage

delegator = Delegator(Target())
delegator.do_something('surf')
delegator.do_anything()
