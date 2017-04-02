# -*- coding: utf-8 -*-

import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    def __new__(cls):
        return cls.get_instance()

    @staticmethod
    def get_instance():
        """get this instance from another thread is fine"""
        if not hasattr(Singleton, '_instance'):
            with Singleton._instance_lock:
                if not hasattr(Singleton, '_instance'):
                    # new instance after double check
                    Singleton._instance = \
                        super(Singleton, Singleton).__new__(Singleton)
        return Singleton._instance


# usage

a = Singleton()
a.name = 'alice'

b = Singleton()
print(b.name)

assert id(a) == id(b)
