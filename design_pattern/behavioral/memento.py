# -*- coding: utf-8 -*-

"""
Memento Pattern


Real world example

Take the example of calculator (i.e. originator), where whenever you perform 
some calculation the last calculation is saved in memory (i.e. memento) so 
that you can get back to it and maybe get it restored using some action 
buttons (i.e. caretaker).


In plain words

Memento pattern is about capturing and storing the current state of an 
object in a manner that it can be restored later on in a smooth manner.


Wikipedia says

The memento pattern is a software design pattern that provides the ability 
to restore an object to its previous state (undo via rollback).
"""


class EditorMemento(object):
    def __init__(self, content):
        self.content = content


class Editor(object):
    def __init__(self):
        self.content = ''

    def write(self, words):
        self.content += words

    def save(self):
        return EditorMemento(self.content)

    def restore(self, editor_memento):
        self.content = editor_memento.content


# usage

editor = Editor()
editor.write('hello')
print(editor.content)

memento = editor.save()

editor.write('#asd77&h as')
print(editor.content)

editor.restore(memento)
print(editor.content)
