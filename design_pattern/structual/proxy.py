# -*- coding: utf-8 -*-


"""
Proxy Pattern


Real world example

Have you ever used an access card to go through a door? There are multiple 
options to open that door i.e. it can be opened either using access card or 
by pressing a button that bypasses the security. The door's main 
functionality is to open but there is a proxy added on top of it to add some 
functionality. Let me better explain it using the code example below.


In plain words

Using the proxy pattern, a class represents the functionality of another class.


Wikipedia says

A proxy, in its most general form, is a class functioning as an interface to 
something else. A proxy is a wrapper or agent object that is being called by 
the client to access the real serving object behind the scenes. Use of the 
proxy can simply be forwarding to the real object, or can provide additional 
logic. In the proxy extra functionality can be provided, for example caching 
when operations on the real object are resource intensive, or checking 
preconditions before operations on the real object are invoked.
"""


class Image(object):
    def display_image(self):
        raise NotImplementedError()


class RealImage(Image):
    def __init__(self, filename):
        self.filename = filename

    def display_image(self):
        print('Displaying ' + self.filename)


class ProxyImage(Image):
    def __init__(self, filename):
        self.filename = filename
        self.image = None

    def display_image(self):
        if not self.image:
            self.image = RealImage(self.filename)
        self.image.display_image()


# usage

image1 = ProxyImage('photo1.png')
image2 = ProxyImage('photo2.png')
image1.display_image()
image2.display_image()
